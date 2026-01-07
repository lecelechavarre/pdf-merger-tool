@echo off
REM PDF Merger Tool Installation Script for Windows
REM This script sets up the PDF merger tool with optional drag and drop support

echo 📄 PDF Merger Tool - Installation Script
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed. Please install Python 3.7 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv pdf_merger_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call pdf_merger_env\Scripts\activate.bat

REM Install core dependencies
echo 📚 Installing core dependencies...
pip install pypdf

REM Optional: Install tkinterdnd2 for drag and drop
echo.
echo 🎯 Optional: Install drag and drop support?
echo    This requires tkinterdnd2 which may need additional system dependencies.
echo    The app will work fine without it - you'll just use the 'Add Files' button.
echo.
set /p install_dragdrop="   Install drag and drop support? (y/N): "
if /i "%install_dragdrop%"=="y" (
    echo 📦 Installing tkinterdnd2...
    pip install tkinterdnd2
    if %errorlevel% equ 0 (
        echo ✅ Drag and drop support installed successfully!
    ) else (
        echo ⚠️  tkinterdnd2 installation failed. The app will still work without drag and drop.
        echo    You can try installing it manually later if needed.
    )
) else (
    echo ⏭️  Skipping drag and drop support ^(optional^).
)

echo.
echo 🎉 Installation complete!
echo.
echo 📋 Usage:
echo    GUI version:    python pdf_merger.py
echo    CLI version:    python pdf_merger_cli.py --help
echo.
echo 📖 For more information, see README.md
echo.
echo 💡 Note: The GUI version requires a graphical desktop environment.
echo    The CLI version works in any terminal environment.
echo.
pause