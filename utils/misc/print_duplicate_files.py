import os
import argparse

def find_duplicates(dir1, dir2):
    """
    Compares two directories and prints the names of files that exist in both.
    """
    if not os.path.isdir(dir1):
        print(f"Error: '{dir1}' is not a valid directory.")
        return
    if not os.path.isdir(dir2):
        print(f"Error: '{dir2}' is not a valid directory.")
        return

    # List all files in both directories (excluding directories themselves)
    files_dir1 = {f for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))}
    files_dir2 = {f for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))}

    # Find the intersection of both sets
    duplicates = files_dir1.intersection(files_dir2)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate files in '{dir1}' and '{dir2}':")
        for filename in sorted(duplicates):
            print(f" - {filename}")
    else:
        print(f"No duplicate files found between '{dir1}' and '{dir2}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate filenames between two directories.")
    parser.add_argument("dir1", help="Path to the first directory.")
    parser.add_argument("dir2", help="Path to the second directory.")

    args = parser.parse_args()

    find_duplicates(args.dir1, args.dir2)
