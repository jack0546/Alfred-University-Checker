@echo off
REM Quick setup script for Ghana University Admission Checker on Windows

echo ================================
echo Ghana Admission Checker Setup
echo ================================
echo.

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo OK Python detected: %python_version%
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo OK Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo OK Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo OK Dependencies installed
echo.

REM Create necessary directories
echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist instance mkdir instance
echo OK Directories created
echo.

echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the application, run:
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
pause
