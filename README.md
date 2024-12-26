# PDF Splitter

A lightweight, user-friendly desktop application for splitting PDF files into smaller documents with equal page counts.

## Features

- **Simple Interface**: Clean, dark-themed UI that's easy to use
- **Secure Processing**: Uses PyMuPDF for secure and efficient PDF handling
- **File Safety**: Warns before overwriting existing files
- **Smart Splitting**: Suggests optimal split sizes for even page distribution
- **Progress Tracking**: Visual progress bar shows splitting progress

## Requirements

- Python 3.x
- PyMuPDF (fitz)
- tkinter

## Installation

1. Install the required package:

```bash
pip install -r requirements.txt
```

2. Run the application

```bash
python pdf_splitter.py
```


## Usage

1. Click "Browse" to select your input PDF file
2. Choose an output folder for the split PDFs
3. Enter the number of pages you want in each split
4. Click "Split PDF" to start the process

The application will:
- Validate your input PDF
- Check if the split size evenly divides the total pages
- Warn you about any existing files that might be overwritten
- Create numbered PDFs (e.g., document_1.pdf, document_2.pdf, etc.)

## Limitations

- File format: PDF only
- Requires read/write permissions in the output directory

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --clean --name PDFSplitter pdf_splitter.py
```
The file will be available in the ```dist/``` directory.

## Security Features

- No system modifications required
- No registry access needed
- No elevated privileges required
- Safe file handling with proper validation
- Memory-efficient processing

## Notes

- The application will suggest optimal split sizes if your chosen page count doesn't evenly divide the total pages
- Progress bar indicates splitting progress
- Dark theme for reduced eye strain
- All split operations are reversible (original file is never modified)