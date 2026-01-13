PDF Scraper
===========

Simple Python script to download all PDF files linked from a single webpage.

Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Usage

```bash
python scraper.py https://example.com/page-with-pdfs
```

Options

- `-o`, `--out` : output directory (default: `downloads`)
- `--check` : perform HEAD checks on non-.pdf links to detect PDFs via Content-Type
- `--timeout` : network timeout in seconds (default: 15)

Example

```bash
python scraper.py https://example.com -o my-pdfs --check
```

Notes

Use responsibly and respect robots.txt / site terms. For large crawls, add rate limiting and politeness headers.
