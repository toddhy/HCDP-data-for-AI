import os
import re
import time
import requests
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from unpywall import Unpywall
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global Settings
MANUAL_MODE = True  # Set to True to handle captchas/sign-ins manually
UNPAYWALL_EMAIL = os.getenv("UNPAYWALL_EMAIL", "example@example.com")
os.environ["UNPAYWALL_EMAIL"] = UNPAYWALL_EMAIL

# Domains that often hang or block direct requests (Tier 1)
DOMAINS_TO_SKIP_TIER1 = [
    "onlinelibrary.wiley.com",
    "sciencedirect.com",
    "linkinghub.elsevier.com",
    "link.springer.com",
    "nature.com",
    "pnas.org",
    "academic.oup.com",
    "journals.ametsoc.org"
]

class RobustDownloader:
    def __init__(self, output_dir="downloads", user_data_dir="browser_session"):
        self.output_dir = output_dir
        self.user_data_dir = user_data_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def sanitize_filename(self, text):
        return re.sub(r'[\\/*?:"<>|]', "", text)[:100]

    def download_direct(self, url, filename):
        """Tier 1: Direct download using requests."""
        try:
            print(f"  [Tier 1] Attempting direct download: {url}", flush=True)
            response = self.session.get(url, timeout=15, stream=True)
            if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", "").lower():
                path = os.path.join(self.output_dir, f"{filename}.pdf")
                with open(path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  [Success] Saved to {path}", flush=True)
                return True
        except Exception as e:
            print(f"  [Tier 1 Failed] {e}", flush=True)
        return False

    def check_unpaywall(self, title):
        """Tier 2: Check Unpaywall for Open Access version."""
        # Note: Unpaywall works best with DOIs. Finding DOI from title is a separate step.
        # For now, we'll focus on browser-based discovery if Tier 1 fails.
        # This can be expanded with Crossref to get DOI first.
        return None

    def download_with_browser(self, url, filename, manual_mode=True):
        """Tier 3: Use Playwright to find PDF on landing page."""
        print(f"  [Tier 3] Using browser for: {url}", flush=True)
        
        with sync_playwright() as p:
            browser = None
            try:
                # Use launch_persistent_context to save sign-in sessions
                try:
                    browser = p.chromium.launch_persistent_context(
                        user_data_dir=self.user_data_dir,
                        headless=not manual_mode,
                        slow_mo=500 if manual_mode else 0,
                        args=['--disable-blink-features=AutomationControlled'], # Help bypass detection
                        accept_downloads=True # Ensure downloads are enabled
                    )
                except Exception as e:
                    print(f"  [Browser Error] Failed to launch browser: {e}", flush=True)
                    print("  [Action] Is another instance of the browser or script running? Close it and try again.", flush=True)
                    return False

                page = browser.new_page()
                
                # Shared state for tracking
                captured_urls = set()
                active_downloads = []

                def save_bytes_as_pdf(url, body, suggested_name=None):
                    if not url or url in captured_urls: return False
                    
                    # Try to get a clean name
                    clean_name = suggested_name or downloader.sanitize_filename(urlparse(url).path.split('/')[-1])
                    if not clean_name.lower().endswith(".pdf"): clean_name += ".pdf"
                    
                    save_path = os.path.abspath(os.path.join(self.output_dir, clean_name))
                    
                    # Handle existing
                    base, ext = os.path.splitext(save_path)
                    counter = 1
                    while os.path.exists(save_path):
                        save_path = f"{base}_{counter}{ext}"
                        counter += 1

                    print(f"  [Capture] Captured via Stream/View: {os.path.basename(save_path)}", flush=True)
                    try:
                        with open(save_path, "wb") as f:
                            f.write(body)
                        captured_urls.add(url)
                        print(f"  [Success] Saved to {save_path}", flush=True)
                        return True
                    except Exception as e:
                        print(f"  [Error] Failed to save PDF: {e}", flush=True)
                        return False

                # STREAME/VIEW CAPTURE: Handler for responses (watching for PDFs in any tab/view)
                def handle_response(response):
                    try:
                        content_type = response.headers.get("content-type", "").lower()
                        if "application/pdf" in content_type:
                            url = response.url
                            if url not in captured_urls:
                                try:
                                    # Attempt to get body
                                    body = response.body()
                                    save_bytes_as_pdf(url, body)
                                except:
                                    pass
                    except:
                        pass

                # OFFICIAL DOWNLOAD CAPTURE: Handler for downloads (standard 'Save As' / Attachment)
                # Following pattern from: https://playwright.dev/docs/downloads
                def handle_download(download):
                    suggested = download.suggested_filename
                    print(f"  [Browser Download] Started: {suggested}", flush=True)
                    active_downloads.append(download)
                    try:
                        # Construct absolute path for save_as
                        save_path = os.path.abspath(os.path.join(self.output_dir, suggested))
                        
                        # Handle collision
                        base, ext = os.path.splitext(save_path)
                        counter = 1
                        while os.path.exists(save_path):
                            save_path = f"{base}_{counter}{ext}"
                            counter += 1
                        
                        # Use official save_as method
                        download.save_as(save_path)
                        print(f"  [Success] Saved browser download to {save_path}", flush=True)
                    except Exception as e:
                        print(f"  [Browser Download Error] {e}", flush=True)
                    finally:
                        if download in active_downloads:
                            active_downloads.remove(download)

                def setup_page(p):
                    # Attach standard listener to every page as per docs
                    p.on("download", handle_download)
                    p.on("response", handle_response)
                
                # Listen for any new tabs/pages opened in this context
                browser.on("page", setup_page)
                setup_page(page) # Initial page

                if manual_mode:
                    print(f"\n  [Manual Mode] Waiting for interaction on: {filename}", flush=True)
                    print("  [Manual Mode] - If you click 'Download', it will save to your downloads folder.", flush=True)
                    print("  [Manual Mode] - If you just 'View' the PDF, the script will capture it too.", flush=True)
                    print("  [Manual Mode] - Once you see '[Success]' above, you can press Enter.", flush=True)
                
                # Navigate
                try:
                    page.goto(url, wait_until="commit", timeout=45000)
                except Exception as ex:
                    print(f"  [Browser Warning] Initial navigation slow: {ex}", flush=True)

                if manual_mode:
                    input("  [Manual Pass] Press Enter here only after the file has been successfully captured...")
                
                # Final wait for active downloads to flush
                if active_downloads:
                    print(f"  [Wait] Finishing {len(active_downloads)} active download(s)...", flush=True)
                    start_wait = time.time()
                    while active_downloads and (time.time() - start_wait < 60):
                        time.sleep(1)
                    if not active_downloads:
                        return True

                # Consider success if we got at least one capture
                if captured_urls:
                    return True

                # Automated Fallback Search
                pdf_selectors = [
                    "a[href$='.pdf']",
                    "a:has-text('PDF')",
                    "a:has-text('Download PDF')",
                    "button:has-text('PDF')",
                    "i.fa-file-pdf",
                    ".pdf-link"
                ]
                
                pdf_url = None
                # Check current URL first
                if ".pdf" in page.url.lower():
                    pdf_url = page.url

                if not pdf_url:
                    for selector in pdf_selectors:
                        try:
                            element = page.query_selector(selector)
                            if element:
                                href = element.get_attribute("href")
                                if href:
                                    pdf_url = page.evaluate("url => new URL(url, document.baseURI).href", href)
                                    if pdf_url: break
                        except:
                            continue
                
                if pdf_url:
                    # Attempt to download the found URL
                    return self.download_direct(pdf_url, filename)
                
                print("  [Tier 3 Failed] Could not find PDF link automatically.", flush=True)
                if not manual_mode:
                    print("  [Action] Try running in manual mode for this link.", flush=True)
                
            except Exception as e:
                print(f"  [Tier 3 Error] {e}", flush=True)
            finally:
                if browser:
                    try:
                        browser.close()
                    except:
                        pass
        return False

def parse_results(file_path):
    papers = []
    current_paper = {}
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Title:"):
                if current_paper:
                    papers.append(current_paper)
                current_paper = {"title": line[6:].strip(), "links": []}
            elif line.startswith("Main Link:"):
                current_paper["main_link"] = line[10:].strip()
            elif line.startswith("[PDF]:"):
                current_paper["pdf_link"] = line[6:].strip()
            elif line.startswith("---") and current_paper:
                papers.append(current_paper)
                current_paper = {}
                
    if current_paper:
        papers.append(current_paper)
        
    return papers

def main():
    results_file = "scholar_results.txt"
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found.")
        return

    downloader = RobustDownloader()
    papers = parse_results(results_file)
    print(f"Found {len(papers)} papers in results.")

    for i, paper in enumerate(papers):
        title = paper.get("title", f"paper_{i}")
        safe_title = downloader.sanitize_filename(title)
        print(f"\n[{i+1}/{len(papers)}] Processing: {title}", flush=True)
        
        # Check if already exists
        if os.path.exists(os.path.join(downloader.output_dir, f"{safe_title}.pdf")):
            print(f"  [Skip] {safe_title}.pdf already exists.", flush=True)
            continue

        success = False
        
        # Check if we should skip Tier 1 for this domain
        def should_skip_tier1(url):
            if not url or url == "None": return True
            parsed = urlparse(url)
            return any(domain in parsed.netloc for domain in DOMAINS_TO_SKIP_TIER1)

        # Try PDF link if available
        pdf_url = paper.get("pdf_link", "None")
        if pdf_url != "None":
            if should_skip_tier1(pdf_url):
                print(f"  [Tier 1 Skip] Difficult domain detected for PDF link.", flush=True)
            else:
                success = downloader.download_direct(pdf_url, safe_title)
        
        # Try Main link if PDF link failed or wasn't available
        main_url = paper.get("main_link", "None")
        if not success and main_url != "None":
            # Always use Tier 3 for main links as they are landing pages
            success = downloader.download_with_browser(main_url, safe_title, manual_mode=MANUAL_MODE)
            
            # If it failed, optionally ask user for manual mode (or skip and log)
            if not success:
                print(f"  [Warning] Automated download failed for: {title}")
                # We could prompt here, but for bulk we should probably log and move on
                # or have a separate "manual pass" script.

    print("\n--- All papers processed ---")

if __name__ == "__main__":
    main()
