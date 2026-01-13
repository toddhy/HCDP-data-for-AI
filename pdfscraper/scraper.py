#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm


def collect_pdf_links(url, check_content_type=False, timeout=15):
    """Return a set of absolute URLs that point to PDF files found on the page.

    If `check_content_type` is True, a HEAD request is used to detect PDFs
    for links that don't end with .pdf.
    """
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue
        full = urljoin(url, href)
        # Quick check by extension
        if full.lower().split('?')[0].endswith('.pdf'):
            links.add(full)
            continue
        # Optional: HEAD to check Content-Type
        if check_content_type:
            try:
                h = requests.head(full, allow_redirects=True, timeout=timeout)
                ctype = h.headers.get('content-type', '')
                if 'application/pdf' in ctype.lower():
                    links.add(full)
            except requests.RequestException:
                # ignore HEAD failures
                continue
    return links


def unique_filename(path, existing):
    """Return a filename that doesn't collide with `existing` set."""
    base = os.path.basename(urlparse(path).path) or 'download'
    name = base
    i = 1
    while name in existing or os.path.exists(name):
        name = f"{os.path.splitext(base)[0]}_{i}{os.path.splitext(base)[1]}"
        i += 1
    return name


def download_file(url, out_dir, timeout=30):
    os.makedirs(out_dir, exist_ok=True)
    # Try to derive filename
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or None
    # Use HEAD to try get filename from headers if missing
    try:
        head = requests.head(url, allow_redirects=True, timeout=timeout)
        if not filename:
            cd = head.headers.get('content-disposition')
            if cd and 'filename=' in cd:
                filename = cd.split('filename=')[-1].strip(' \"')
    except requests.RequestException:
        head = None
    if not filename:
        filename = os.path.basename(parsed.path) or 'file.pdf'
    # Ensure unique
    existing = set(os.listdir(out_dir))
    outname = filename
    if outname in existing:
        base, ext = os.path.splitext(filename)
        i = 1
        while outname in existing:
            outname = f"{base}_{i}{ext}"
            i += 1
    outpath = os.path.join(out_dir, outname)

    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length') or 0)
        chunk_size = 8192
        with open(outpath, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True, desc=outname, leave=False) as pbar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    return outpath


def main():
    parser = argparse.ArgumentParser(description='Download all PDF files linked from a webpage')
    parser.add_argument('url', help='Page URL to scan for PDFs')
    parser.add_argument('-o', '--out', default='downloads', help='Output directory')
    parser.add_argument('--check', action='store_true', help='HEAD-check non-.pdf links for Content-Type')
    parser.add_argument('--timeout', type=int, default=15, help='Network timeout (seconds)')
    args = parser.parse_args()

    try:
        pdfs = collect_pdf_links(args.url, check_content_type=args.check, timeout=args.timeout)
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        sys.exit(1)

    if not pdfs:
        print("No PDF links found.")
        return

    print(f"Found {len(pdfs)} PDF(s). Downloading to '{args.out}'")
    downloaded = []
    for url in pdfs:
        try:
            path = download_file(url, args.out, timeout=max(args.timeout, 30))
            downloaded.append(path)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    print(f"Done. {len(downloaded)} files saved in '{args.out}'")


if __name__ == '__main__':
    main()
