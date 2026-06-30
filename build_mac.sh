#!/bin/bash
echo "========================================"
echo "Building macOS Launcher..."
echo "========================================"

echo "1. Installing dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "2. Please ensure you have placed miniserve-mac-x64 binaries in the 'bin' folder!"
echo "   Making miniserve executable..."
chmod +x bin/miniserve-mac-x64

echo "3. Building with PyInstaller..."
# -y: yes to all prompts
# -F: onefile
# -w: windowed (no console)
python3 -m PyInstaller -y -F -w --name "MiniServe" --add-data "bin:bin" main.py

echo ""
echo "========================================"
echo "Build complete! Check the dist folder for MiniServe.app"
echo "========================================"
