#!/usr/bin/env python3
"""
Command-line PDF Merger Tool
A simple CLI tool to merge multiple PDF files into one using pypdf.
"""

import argparse
import os
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs(output_path: str, pdf_files: list, verbose: bool = False) -> bool:
    """
    Merge multiple PDF files into one.
    
    Args:
        output_path: Path for the output PDF file
        pdf_files: List of PDF file paths to merge
        verbose: Whether to show detailed progress
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if verbose:
            print(f"Starting PDF merge process...")
            print(f"Output file: {output_path}")
            print(f"Input files: {len(pdf_files)}")
        
        # Validate input files
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                print(f"Error: File not found: {pdf_file}")
                return False
            
            if not pdf_file.lower().endswith('.pdf'):
                print(f"Error: Not a PDF file: {pdf_file}")
                return False
        
        # Create PDF writer
        writer = PdfWriter()
        total_pages = 0
        
        # Process each PDF file
        for i, pdf_file in enumerate(pdf_files, 1):
            if verbose:
                print(f"Processing file {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
            
            try:
                reader = PdfReader(pdf_file)
                file_pages = len(reader.pages)
                total_pages += file_pages
                
                if verbose:
                    print(f"  - Adding {file_pages} pages")
                
                # Add all pages to writer
                for page in reader.pages:
                    writer.add_page(page)
                    
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
                return False
        
        # Write merged PDF
        if verbose:
            print(f"Writing merged PDF with {total_pages} total pages...")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'wb') as output:
            writer.write(output)
        
        print(f"✅ Successfully merged {len(pdf_files)} files ({total_pages} pages) into:")
        print(f"   {output_path}")
        
        # Show file size
        file_size = os.path.getsize(output_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if file_size < 1024.0:
                print(f"   File size: {file_size:.1f} {unit}")
                break
            file_size /= 1024.0
        
        return True
        
    except Exception as e:
        print(f"❌ Error merging PDFs: {e}")
        return False


def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -o output.pdf file1.pdf file2.pdf file3.pdf
  %(prog)s -o merged.pdf --verbose *.pdf
  %(prog)s -o result.pdf --sort file1.pdf file3.pdf file2.pdf
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='PDF files to merge'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file path'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed progress information'
    )
    
    parser.add_argument(
        '--sort',
        action='store_true',
        help='Sort input files alphabetically before merging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PDF Merger CLI 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if len(args.files) < 2:
        print("Error: At least 2 PDF files are required for merging.")
        sys.exit(1)
    
    # Sort files if requested
    if args.sort:
        args.files.sort()
        if args.verbose:
            print("Files sorted alphabetically:")
            for i, file in enumerate(args.files, 1):
                print(f"  {i}. {file}")
    
    # Check if output file already exists
    if os.path.exists(args.output):
        response = input(f"Output file '{args.output}' already exists. Overwrite? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            sys.exit(0)
    
    # Merge PDFs
    success = merge_pdfs(args.output, args.files, args.verbose)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()