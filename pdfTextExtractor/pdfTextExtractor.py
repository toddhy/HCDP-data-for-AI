import pathlib, pymupdf

#Choose directory containing pdf files
input_dir = "C:\SCIPE\CitationPapers\Mapping daily air temperature" 

# Iterate through all .pdf files in the directory
for pdf_path in pathlib.Path(input_dir).glob("*.pdf"):
    print(f"Extracting: {pdf_path.name}")
    
    try:
        with pymupdf.open(pdf_path) as doc:
            text = chr(12).join([page.get_text() for page in doc])
        
        # Save output in the same directory as [filename].pdf.txt
        output_path = pdf_path.with_suffix(pdf_path.suffix + ".txt")
        output_path.write_bytes(text.encode())
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")