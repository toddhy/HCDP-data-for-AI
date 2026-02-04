import os
import argparse
import shutil
from pathlib import Path

def get_titles(directory_path):
    """
    Reads all files in a given directory and returns a set of titles
    (filenames stripped after the first dot).
    """
    path = Path(directory_path)
    if not path.is_dir():
        print(f"Error: The directory '{directory_path}' does not exist or is not a directory.")
        return set()

    files = [f for f in path.iterdir() if f.is_file()]
    return {f.name.split('.')[0] for f in files}

def sync_files(source_dir, search_dir):
    """
    Gets titles from source_dir, searches search_dir for files with matching titles,
    and copies them to the current directory.
    """
    titles = get_titles(source_dir)
    if not titles:
        return

    search_path = Path(search_dir)
    if not search_path.is_dir():
        print(f"Error: The directory '{search_dir}' does not exist or is not a directory.")
        return

    print(f"Searching '{search_dir}' for files matching titles from '{source_dir}'...")
    
    found_any = False
    for file in search_path.iterdir():
        if file.is_file():
            title = file.name.split('.')[0]
            if title in titles:
                print(f"Found match: {file.name}. Copying to current directory...")
                try:
                    shutil.copy2(file, Path.cwd())
                    found_any = True
                except Exception as e:
                    print(f"Failed to copy {file.name}: {e}")

    if not found_any:
        print("No matches found in the search directory.")
    else:
        print("Done copying matching files.")

def main():
    parser = argparse.ArgumentParser(description="List titles from a source directory and copy matching files from a search directory.")
    parser.add_argument("source_directory", help="Path to the directory to get titles from")
    parser.add_argument("search_directory", nargs="?", help="Optional second directory to search for matching files and copy them")
    
    args = parser.parse_args()
    
    if args.search_directory:
        sync_files(args.source_directory, args.search_directory)
    else:
        # If no search directory, just list the titles as before
        titles = sorted(list(get_titles(args.source_directory)))
        if titles:
            print(f"Titles of files in '{args.source_directory}':")
            for title in titles:
                print(title)

if __name__ == "__main__":
    main()
