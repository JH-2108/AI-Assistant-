# Multi-Format File Analysis Guide

Jarvis now supports analyzing any type of file through the web interface!

## Supported File Formats

### Documents
- **PDF** - `.pdf` - Full text extraction from all pages
- **Word** - `.docx`, `.doc` - Document and table extraction
- **Excel** - `.xlsx`, `.xls` - Sheet and cell data extraction
- **PowerPoint** - `.pptx`, `.ppt` - Slide content extraction

### Code & Text
- Python, JavaScript, HTML, CSS, JSON, YAML, XML, CSV, Markdown, and more
- Plain text files (`.txt`)
- Configuration files (`.ini`, `.cfg`, `.yml`)

### Images
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`
- Image metadata and dimension information

## Setup Instructions

### 1. Install Required Libraries

```bash
pip install -r requirements_automation.txt
```

This installs:
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX file handling
- **openpyxl** - Excel file handling
- **python-pptx** - PowerPoint file handling
- **pytesseract** - OCR support for scanned/image PDFs
- **pdf2image** - Converts PDF pages into images for OCR

### 1.1 Install Tesseract and Poppler on Windows

1. Install Tesseract from the Windows installer or unzip it to a folder like:
   - `C:\Program Files\Tesseract-OCR`

2. Install Poppler for Windows and unzip it to a folder like:
   - `C:\Users\Lenovo\Downloads\poppler-25.12.0\poppler-25.12.0\Library\bin`

3. Add both folders to your system `PATH`:
   - `C:\Program Files\Tesseract-OCR`
   - `C:\Users\Lenovo\Downloads\poppler-25.12.0\poppler-25.12.0\Library\bin`

4. Restart PowerShell / VS Code after editing `PATH`.

> Note: The app also tries to use Tesseract from `C:\Program Files\Tesseract-OCR\tesseract.exe` and Poppler from the extracted Downloads path above.

5. Verify installation:

```powershell
tesseract --version
where tesseract
```

If `tesseract` is not found, add the exact install path to `PATH` or update `Assistant.py` with the installed `tesseract.exe` location.

### 2. Run Jarvis

```bash
python web_app.py
```

Visit `http://localhost:8765` in your browser.

## How to Use

### Via Web Interface

1. **Click the "+" button** (top-left of input area)
2. **Select any file** (PDF, DOCX, image, code file, etc.)
3. **Optionally enter a request** in the input field:
   - `analyze this PDF` - Get a summary
   - `check for errors` - Review for mistakes
   - `summarize the document` - Get key points
   - Leave empty for automatic review
4. **Click the ⚡ button** to send

### Via Command Line

```python
from Assistant import review_file_content

# For a file on disk
response = review_file_content(
    "myfile.pdf",
    "/path/to/myfile.pdf",
    user_request="Summarize the document",
    is_file_path=True
)
print(response)

# For text content
response = review_file_content(
    "code.py",
    "def hello():\n    print('world')",
    user_request="Check for issues"
)
print(response)
```

## File Size Limits

- **Text uploads**: Max 50,000 characters
- **Binary file uploads** (PDF, DOCX, images): Max 50MB
- **Extracted content**: Max 50,000 characters (for AI analysis)

Files are temporarily stored and automatically deleted after analysis.

## AI Models Used

- **Default Analysis**: `qwen2.5:7b` (fast, efficient)
- **Document Review**: `qwen2.5:1.5b` (ultra-fast, optimized for document analysis)
- **Fallback**: `phi3:mini` (fastest, if other models timeout)

## Features

✅ Automatic file type detection
✅ Multi-page PDF support
✅ Table extraction from DOCX and Excel
✅ Slide content from PowerPoint
✅ Image metadata
✅ Automatic content extraction
✅ Smart timeout handling with fallback models
✅ No file size restrictions on analysis
✅ Automatic cleanup of temporary files

## Example Use Cases

### Analyze a PDF Report
Upload `report.pdf` with request: "What are the key findings?"

### Review Code Files
Upload `app.py` with request: "Check for bugs or improvements"

### Extract Data from Excel
Upload `data.xlsx` with request: "Summarize the sales data"

### Analyze Screenshots
Upload `screenshot.png` with request: "What's happening in this image?"

## Troubleshooting

### "PyPDF2 not installed" error
```bash
pip install PyPDF2
```

### "python-docx not installed" error
```bash
pip install python-docx
```

### "openpyxl not installed" error
```bash
pip install openpyxl
```

### "python-pptx not installed" error
```bash
pip install python-pptx
```

### File analysis taking too long
- The system automatically uses faster models if the primary model is slow
- Larger files take longer to extract and analyze
- Try with a shorter portion of the file

## Performance Tips

1. **For fast analysis**: Let Jarvis auto-review without specifying a request
2. **For large files**: Use the fast document model (qwen2.5:1.5b)
3. **For complex analysis**: Include specific questions to guide the AI
4. **For large PDFs**: Consider analyzing sections separately

---

**Note**: Jarvis extracts content server-side and analyzes it using local AI models. No files are uploaded to external services.
