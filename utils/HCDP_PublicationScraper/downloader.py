import requests
import os
import sys
from urllib.parse import urlparse

def download_file(url, folder):
    """
    Downloads a file from a URL and saves it to the specified folder.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Try to get filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Fallback if no filename in URL
        if not filename:
            filename = "downloaded_file"
            
        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        save_path = os.path.join(folder, filename)
        
        while os.path.exists(save_path):
            filename = f"{base}_{counter}{ext}"
            save_path = os.path.join(folder, filename)
            counter += 1

        print(f"Downloading: {url} -> {filename}")
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print("Dictionary success.")
        return True

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    print("--- Bulk Downloader ---")
    
    # Get input file
    print("Enter the file containing URLs (default: output.txt):")
    input_file = input("> ").strip()
    if not input_file:
        input_file = "output.txt"
        
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Get output directory
    print("Enter the download directory (default: downloads):")
    output_dir = input("> ").strip()
    if not output_dir:
        output_dir = "downloads"

    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory: {e}")
            return

    # Read URLs and download
    print(f"Reading URLs from '{input_file}'...")
    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Found {len(urls)} URLs. Starting download...")
    
    success_count = 0
    for url in urls:
        if download_file(url, output_dir):
            success_count += 1
            
    print(f"\nDownload complete. {success_count}/{len(urls)} files downloaded successfully.")

if __name__ == "__main__":
    main()
