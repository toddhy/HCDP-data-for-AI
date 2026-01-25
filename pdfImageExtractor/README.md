# PDF Image and Text Extraction Tools

This directory contains a suite of Python scripts designed to extract content from PDF files using different methods, ranging from simple image extraction to AI-powered document conversion.

## Scripts Overview

### 1. `run_marker.py`
**AI-Powered PDF to Markdown Conversion**
This is the most advanced tool in the suite. it uses the `marker-pdf` library to convert PDFs into structured Markdown files.

*   **What it does:** Extracts text, tables, and images while preserving the document's layout.
*   **Key Features:**
    *   Saves output in individual subdirectories named after the PDF.
    *   Generates a `.md` file for text and a folder for extracted images.
    *   **Optimized Performance:** Configured with `disable_ocr: True` and `ocr_engine: None` to significantly speed up processing and reduce memory usage by relying on the PDF's native text layer.
*   **Usage:**
    ```bash
    python run_marker.py
    ```
*   **Dependencies:** `marker-pdf`, `torch`, `surya-ocr` (installed via `pip install marker-pdf`).

### 2. `extractImages.py`
**PDF Asset Extraction**
A lightweight script focused on extracting embedded image files from PDF documents.

*   **What it does:** Scans each page of the PDF and saves every individual image asset (photos, charts, icons) as a separate file.
*   **Usage:** Update the `target_directory` variable at the bottom of the script and run:
    ```bash
    python extractImages.py
    ```
*   **Dependencies:** `PyMuPDF` (fitz), `Pillow`.

### 3. `convertToImage.py`
**Full Page Rendering**
Converts entire PDF pages into high-quality images.

*   **What it does:** Renders each page of the PDF as a single PNG image. This is useful if you want to preserve the exact visual appearance of the document.
*   **Usage:** Update the `target_directory` variable at the bottom of the script and run:
    ```bash
    python convertToImage.py
    ```
*   **Dependencies:** `PyMuPDF` (fitz).

---

## Installation

To use these scripts, you will need Python installed. It is recommended to install the dependencies in a virtual environment:

```bash
pip install pymupdf pillow marker-pdf
```

## Summary of Differences

| Tool | Focus | Output Type | Best For |
| :--- | :--- | :--- | :--- |
| **run_marker.py** | Structure & Text | `.md` + Assets | Converting papers/reports to editable text. |
| **extractImages.py** | Embedded Assets | Individual Images | Collecting photos/charts from a PDF. |
| **convertToImage.py** | Visual Preservation | Full Page PNGs | Creating thumbnails or reading-images of pages. |
