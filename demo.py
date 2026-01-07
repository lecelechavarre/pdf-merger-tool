#!/usr/bin/env python3
"""
PDF Merger Demo Script
Demonstrates the PDF merger functionality with sample files
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    print(f"Command: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Main demo function"""
    print("📄 PDF Merger Tool - Live Demo")
    print("=" * 60)
    
    # Check if we're in a virtual environment
    if 'pdf_merger_env' not in sys.executable:
        print("⚠️  Activating virtual environment...")
        if os.path.exists('pdf_merger_env/bin/activate'):
            run_command("source pdf_merger_env/bin/activate", "Activating virtual environment")
    
    # Demo 1: CLI Help
    run_command("python pdf_merger_cli.py --help", "Showing CLI Help")
    
    # Demo 2: Create sample files (if they don't exist)
    if not all(os.path.exists(f) for f in ['sample1.pdf', 'sample2.pdf', 'sample3.pdf']):
        print("\n📝 Creating sample PDF files...")
        run_command("python create_sample_pdfs.py", "Creating sample PDFs")
    
    # Demo 3: Basic merge
    run_command(
        "python pdf_merger_cli.py -o demo_basic.pdf sample1.pdf sample2.pdf", 
        "Basic PDF Merge"
    )
    
    # Demo 4: Verbose merge with sorting
    run_command(
        "python pdf_merger_cli.py -o demo_sorted.pdf --sort --verbose sample3.pdf sample1.pdf sample2.pdf", 
        "Sorted Merge with Verbose Output"
    )
    
    # Demo 5: List output files
    print("\n📋 Generated Files:")
    print("=" * 30)
    for file in ['demo_basic.pdf', 'demo_sorted.pdf']:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} (not found)")
    
    print("\n🎉 Demo completed!")
    print("💡 You can now run the GUI version with: python pdf_merger.py")
    print("   (requires a graphical environment)")

if __name__ == "__main__":
    main()