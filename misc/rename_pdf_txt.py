import os
import argparse
from pathlib import Path

def rename_pdf_txt_files(directory_path):
    """
    Searches a directory for files ending in .pdf.txt and renames them to .txt.
    """
    path = Path(directory_path)
    
    if not path.is_dir():
        print(f"Error: The directory '{directory_path}' does not exist or is not a directory.")
        return

    print(f"Scanning '{directory_path}' for .pdf.txt files...")
    
    count = 0
    for file in path.iterdir():
        if file.is_file() and file.name.lower().endswith('.pdf.txt'):
            # New name: remove .pdf from .pdf.txt
            # Example: paper.pdf.txt -> paper.txt
            new_name = file.name[:-8] + ".txt"
            new_path = file.parent / new_name
            
            # Check if target already exists to avoid overwriting
            if new_path.exists():
                print(f"Skipping '{file.name}': target '{new_name}' already exists.")
                continue
                
            try:
                file.rename(new_path)
                print(f"Renamed: '{file.name}' -> '{new_name}'")
                count += 1
            except Exception as e:
                print(f"Failed to rename '{file.name}': {e}")

    print(f"Finished. Renamed {count} files.")

def main():
    parser = argparse.ArgumentParser(description="Rename files ending in .pdf.txt to .txt in a directory.")
    parser.add_argument("directory", help="Path to the directory containing .pdf.txt files")
    
    args = parser.parse_args()
    
    rename_pdf_txt_files(args.directory)

if __name__ == "__main__":
    main()
