# PDF Merger Tool

A professional desktop application built with Python that allows users to easily merge multiple PDF files into a single document. This tool is perfect for combining resumes, reports, study materials, or any other PDF documents.

## Features

- **Intuitive GUI**: Clean and user-friendly interface built with tkinter
- **Drag & Drop Support**: Simply drag PDF files onto the application window
- **File Management**: Add, remove, and reorder PDF files before merging
- **Progress Tracking**: Real-time progress updates during the merge process
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Robust error handling with informative messages
- **File Information**: Displays file names and sizes in an organized table

## Installation

### Quick Install (Recommended)

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Manual Installation

1. **Clone or download the files**:
   ```bash
   # Download pdf_merger.py, pdf_merger_cli.py, and requirements.txt
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv pdf_merger_env
   source pdf_merger_env/bin/activate  # Linux/macOS
   # or
   pdf_merger_env\Scripts\activate.bat  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Optional - Drag and Drop Support:**
   ```bash
   pip install tkinterdnd2
   ```
   Note: The app works perfectly without drag and drop - you'll just use the "Add Files" button.

4. **tkinter availability**:
   - tkinter usually comes pre-installed with Python
   - If not available, install it based on your system:
     - Ubuntu/Debian: `sudo apt-get install python3-tk`
     - macOS: Should come with Python
     - Windows: Reinstall Python and ensure "tcl/tk and IDLE" is selected

## Usage

1. **Run the application**:
   ```bash
   python pdf_merger.py
   ```

2. **Add PDF files** using any of these methods:
   - Click "Add PDF Files" button and select files
   - Drag and drop PDF files directly onto the application window (if tkinterdnd2 is installed)
   - Multiple files can be selected at once

3. **Organize your files** (optional):
   - Use "Move Up" and "Move Down" buttons to reorder files
   - Select files and click "Remove Selected" to remove specific files
   - Click "Clear All" to remove all files and start over

4. **Merge the files**:
   - Click "Merge PDFs" button
   - Choose where to save the merged file
   - Wait for the process to complete
   - The application will offer to open the merged file when done

## Requirements

- Python 3.7 or higher
- pypdf (for PDF processing)
- tkinterdnd2 (optional, for drag and drop support)

## Dependencies

- **pypdf**: A powerful PDF processing library for reading, writing, and manipulating PDF documents
- **tkinterdnd2**: Enables drag and drop functionality (optional but recommended)

## Error Handling

The application includes comprehensive error handling for:
- Corrupted or password-protected PDF files
- File access permissions
- Disk space issues
- Invalid file formats

## Technical Details

- **Framework**: tkinter (built into Python)
- **PDF Library**: pypdf (modern replacement for PyPDF2)
- **Threading**: Background processing to prevent UI freezing
- **File Validation**: Checks for valid PDF format before processing
- **Memory Management**: Efficient processing of large PDF files

## Example Use Cases

- **Job Applications**: Merge resume, cover letter, and portfolio
- **Academic Work**: Combine research papers, notes, and references
- **Business Reports**: Merge sections from different contributors
- **Study Materials**: Combine lecture notes, slides, and textbooks
- **Legal Documents**: Merge contracts, exhibits, and supporting documents

## Troubleshooting

**Common Issues:**

1. **"ModuleNotFoundError: No module named 'tkinter'"**
   - Install tkinter: `sudo apt-get install python3-tk` (Ubuntu/Debian)
   - On macOS, tkinter should come with Python
   - On Windows, reinstall Python and ensure "tcl/tk and IDLE" is selected

2. **Drag and drop not working**
   - Install tkinterdnd2: `pip install tkinterdnd2`
   - If still not working, use the "Add PDF Files" button instead

3. **"Error processing PDF file"**
   - Check if the PDF is password-protected
   - Ensure the file is not corrupted
   - Try opening the file in a PDF reader first

## License

This project is open source and available under the MIT License.