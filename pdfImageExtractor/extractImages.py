import fitz  # PyMuPDF
from PIL import Image
import io
import os


def extract_images_from_pdf(pdf_path, output_folder=None):
    """Extract all images from a PDF file"""
    pdf_abspath = os.path.abspath(pdf_path)
    pdf_dir = os.path.dirname(pdf_abspath)
    
    # If no output folder is provided, use the PDF's name (without the extension)
    if output_folder is None:
        file_basename = os.path.basename(pdf_abspath)
        output_folder = os.path.splitext(file_basename)[0]

    # Ensure output_folder is an absolute path or relative to pdf_dir
    if not os.path.isabs(output_folder):
        output_folder = os.path.join(pdf_dir, output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    pdf_document = fitz.open(pdf_abspath)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = os.path.join(output_folder, f"page{page_num+1}_img{img_index+1}.{image_ext}")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            
            print(f"Extracted: {image_filename}")
    
    pdf_document.close()


def process_directory(directory_path):
    """Process all PDF files in the specified directory"""
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a directory.")
        return

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"\nProcessing: {pdf_path}")
            extract_images_from_pdf(pdf_path)


# Usage
if __name__ == "__main__":
    target_directory = r"C:\SCIPE\CitationPapers\Optimizing automated kriging to improve spatial interpolation"
    process_directory(target_directory)

