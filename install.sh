#!/bin/bash

# PDF Merger Tool Installation Script
# This script sets up the PDF merger tool with optional drag and drop support

echo "📄 PDF Merger Tool - Installation Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv pdf_merger_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source pdf_merger_env/bin/activate

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install pypdf

# Optional: Install tkinterdnd2 for drag and drop
echo ""
echo "🎯 Optional: Install drag and drop support?"
echo "   This requires tkinterdnd2 which may need additional system dependencies."
echo "   The app will work fine without it - you'll just use the 'Add Files' button."
echo ""
read -p "   Install drag and drop support? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing tkinterdnd2..."
    if pip install tkinterdnd2; then
        echo "✅ Drag and drop support installed successfully!"
    else
        echo "⚠️  tkinterdnd2 installation failed. The app will still work without drag and drop."
        echo "   You can try installing it manually later if needed."
    fi
else
    echo "⏭️  Skipping drag and drop support (optional)."
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Usage:"
echo "   GUI version:    python pdf_merger.py"
echo "   CLI version:    python pdf_merger_cli.py --help"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "💡 Note: The GUI version requires a graphical desktop environment."
echo "   The CLI version works in any terminal environment."