import argparse
from pathlib import Path

def compare_files(directory_path):
    """
    Compares .pdf and .txt files in a directory and prints the differences.
    """
    path = Path(directory_path)
    
    if not path.is_dir():
        print(f"Error: The directory '{directory_path}' does not exist or is not a directory.")
        return

    # Get sets of stems for each extension
    pdf_stems = {f.stem for f in path.iterdir() if f.is_file() and f.suffix.lower() == '.pdf'}
    txt_stems = {f.stem for f in path.iterdir() if f.is_file() and f.suffix.lower() == '.txt'}

    only_in_pdf = sorted(list(pdf_stems - txt_stems))
    only_in_txt = sorted(list(txt_stems - pdf_stems))

    print(f"Comparison for directory: {directory_path}\n")

    if not only_in_pdf and not only_in_txt:
        print("All .pdf and .txt files are perfectly matched.")
        return

    if only_in_pdf:
        print(f"--- Files with .pdf but NO matching .txt ({len(only_in_pdf)}) ---")
        for stem in only_in_pdf:
            print(stem)
        print()

    if only_in_txt:
        print(f"--- Files with .txt but NO matching .pdf ({len(only_in_txt)}) ---")
        for stem in only_in_txt:
            print(stem)
        print()

def main():
    parser = argparse.ArgumentParser(description="Compare .pdf and .txt files in a directory to find mismatches.")
    parser.add_argument("directory", help="Path to the directory to compare")
    
    args = parser.parse_args()
    
    compare_files(args.directory)

if __name__ == "__main__":
    main()
