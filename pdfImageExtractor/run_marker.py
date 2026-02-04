import os
import argparse

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import save_output


# Initialize the converter once (this part is slow, so we do it outside the loop)
print("Loading AI models")
converter = PdfConverter(
    artifact_dict=create_model_dict(),
)

def main():
    # command line argument for source directory
    parser = argparse.ArgumentParser(description="Convert PDF files in a directory to text/data using the marker tool.")
    parser.add_argument("source_dir", help="Path to the folder containing your PDFs")
    parser.add_argument("--start", type=int, default=0, help="Index of the first PDF to process (0-indexed, default: 0)")
    parser.add_argument("--count", type=int, help="Number of PDFs to process (default: all files from start index)")
    
    args = parser.parse_args()
    source_dir = args.source_dir

    # Get and sort all PDF files in the folder
    all_files = sorted([f for f in os.listdir(source_dir) if f.lower().endswith(".pdf")])
    
    if not all_files:
        print(f"No PDF files found in '{source_dir}'.")
        return

    # Slice the list based on start and count
    end_index = args.start + args.count if args.count is not None else None
    files_to_process = all_files[args.start : end_index]

    if not files_to_process:
        print(f"No files to process for start index {args.start} and count {args.count}.")
        return

    # Define where to save the results
    output_dir = os.path.join(source_dir, "marker_output")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📂 Found {len(all_files)} total PDF(s).")
    print(f"▶️ Starting from index {args.start}. Processing {len(files_to_process)} file(s).")

    # Loop through the subset of files
    for filename in files_to_process:
        full_path = os.path.join(source_dir, filename)
        print(f"\n🚀 Processing: {filename}...")
        
        try:
            # Convert the PDF to text/data
            rendered = converter(full_path)
            
            # Create a specific folder for this file's output
            fname_base = os.path.splitext(filename)[0]
            file_specific_dir = os.path.join(output_dir, fname_base)
            os.makedirs(file_specific_dir, exist_ok=True)
            
            # Save the output (text, images, etc.) to the file-specific directory
            save_output(rendered, file_specific_dir, fname_base)
            
            print(f"✅ Success! Saved output for {filename} to {file_specific_dir}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    main()

