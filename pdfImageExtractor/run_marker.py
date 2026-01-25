import os
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import save_output


# Initialize config with OCR disabled for faster processing
config_dict = {
    "disable_ocr": True,
    "ocr_engine": None
}

# Initialize the converter once (this part is slow, so we do it outside the loop)
print("Loading AI models (OCR disabled)...")
converter = PdfConverter(
    artifact_dict=create_model_dict(),
    config=config_dict,
)




# Define the folder containing your PDFs
source_dir = r"C:\SCIPE\HCDP-data-for-AI\pdfImageExtractor"
# Define where to save the results
output_dir = os.path.join(source_dir, "marker_output")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all files in the folder
for filename in os.listdir(source_dir):
    # Check if the file is a PDF
    if filename.lower().endswith(".pdf"):
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

