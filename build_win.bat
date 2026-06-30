@echo off
echo ========================================
echo Building Windows Launcher...
echo ========================================

echo 1. Installing dependencies...
py -m pip install -r requirements.txt

echo.
echo 2. Skipping automatic download. Please ensure you have placed miniserve binaries in the 'bin' folder!
echo 3. Building with PyInstaller...
py -m PyInstaller -y -F -w --name "MiniServe" --add-data "bin;bin" main.py

echo.
echo ========================================
echo Build complete! Check the dist folder for MiniServe.exe
echo ========================================
pause
