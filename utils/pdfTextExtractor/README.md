Script iterates through all .pdf files in a directory and extracts text from each file. The extracted text is saved in a new file with the same name as the original file, but with a .txt extension. 

To run the script, install pymupdf first:
```pip -m install pymupdf```

Edit the script and change the input directory to the directory containing the .pdf files you want to extract text from.

Then run the script:
```python pdfTextExtractor.py```

Text files will be saved in the same directory as the original .pdf files.
