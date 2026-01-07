#!/usr/bin/env python3
"""
Test script to create sample PDF files for testing the PDF merger
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_pdf(filename, content, page_count=1):
    """Create a sample PDF file"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for page in range(page_count):
        c.drawString(100, height - 100, f"Sample PDF: {filename}")
        c.drawString(100, height - 130, f"Page: {page + 1} of {page_count}")
        c.drawString(100, height - 160, content)
        
        if page < page_count - 1:
            c.showPage()
    
    c.save()
    print(f"Created: {filename}")

def main():
    """Create sample PDF files for testing"""
    print("Creating sample PDF files for testing...")
    
    # Create sample files
    create_sample_pdf("sample1.pdf", "This is the first sample PDF file.\nIt contains some test content.\nPerfect for testing the PDF merger!", 2)
    create_sample_pdf("sample2.pdf", "This is the second sample PDF.\nIt has different content to test merging.\nThe merger should combine these files properly.", 1)
    create_sample_pdf("sample3.pdf", "Third sample PDF with more content.\nTesting how the merger handles multiple files.\nEach file should appear in order.", 3)
    
    print("\nSample files created successfully!")
    print("You can now test the PDF merger with:")
    print("  python pdf_merger_cli.py -o merged.pdf sample1.pdf sample2.pdf sample3.pdf --verbose")

if __name__ == "__main__":
    main()