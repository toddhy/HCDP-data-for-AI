import fitz  # PyMuPDF
from PIL import Image
import io
import os


def extract_images_from_pdf(pdf_path, output_folder=None):
    """Extract all images from a PDF file"""
    # If no output folder is provided, use the PDF's name (without the extension)
    if output_folder is None:
        file_basename = os.path.basename(pdf_path)
        output_folder = os.path.splitext(file_basename)[0]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = f"{output_folder}/page{page_num+1}_img{img_index+1}.{image_ext}"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            
            print(f"Extracted: {image_filename}")
    
    pdf_document.close()


# Usage
extract_images_from_pdf(r"C:\SCIPE\HCDP-data-for-AI\001_The Hawai 'i climate data portal (HCDP)_2024.pdf")

