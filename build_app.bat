@echo off
echo Building Capture Image Tool...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build the executable
echo Creating executable...
pyinstaller --onefile --windowed --name "CaptureImageTool" --icon=NONE capture.py

echo.
if %errorlevel% equ 0 (
    echo Build completed successfully!
    echo Executable is located in the 'dist' folder
) else (
    echo Build failed. Please check the error messages above.
)

pause
