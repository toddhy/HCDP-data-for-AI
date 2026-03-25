import fitz  # PyMuPDF
import os

def render_pdf_to_images(pdf_path, output_folder=None):
    """Render each page of a PDF as a PNG image"""
    pdf_abspath = os.path.abspath(pdf_path)
    pdf_dir = os.path.dirname(pdf_abspath)
    
    # Derive output folder from PDF name if not provided
    if output_folder is None:
        file_basename = os.path.basename(pdf_abspath)
        output_folder = os.path.splitext(file_basename)[0] + "_pages"

    # Ensure output_folder is joined with pdf_dir if it's a relative path
    if not os.path.isabs(output_folder):
        output_folder = os.path.join(pdf_dir, output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    doc = fitz.open(pdf_abspath)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render page to a pixmap (image)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
        
        image_filename = os.path.join(output_folder, f"page_{page_num+1}.png")
        pix.save(image_filename)
        print(f"Rendered: {image_filename}")
        
    doc.close()

def process_directory_rendering(directory_path):
    """Process all PDF files in the specified directory and render their pages"""
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a directory.")
        return

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"\nRendering PDF: {pdf_path}")
            render_pdf_to_images(pdf_path)

# Usage
if __name__ == "__main__":
    # Update this path to your target directory
    target_directory = r"C:\SCIPE\HCDP-data-for-AI\pdfImageExtractor"
    process_directory_rendering(target_directory)