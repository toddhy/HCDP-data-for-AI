import pathlib
import argparse
import sys
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Upload .txt files to GenAI File API")
    parser.add_argument("--path", type=str, required=True, help="Path to search for .txt files")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()

    client = genai.Client()
    MODEL_ID = "gemini-2.5-flash"

    files = []
    path_to_search = args.path
    print(f"Uploading files from {path_to_search}...")

    # Searching for .txt files
    search_path = pathlib.Path(path_to_search)
    if not search_path.exists():
        print(f"Error: Path {path_to_search} does not exist.")
        return

    for p in search_path.rglob('*.txt'):
        if 'test' in str(p):
            continue
        try:
            f = client.files.upload(file=p, config={'display_name': p.name})
            files.append(f)
            print('.', end='', flush=True)
        except Exception as e:
            print(f"\nError uploading {p}: {e}")

    if not files:
        print("\nNo .txt files found! Check the directory path and file extension.")
        return

    print(f"\nUploaded {len(files)} files.")

    

if __name__ == "__main__":
    main()