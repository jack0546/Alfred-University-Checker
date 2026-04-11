@echo off
REM Ghana Admission Checker - Windows Startup Script

cls
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Ghana University Admission Eligibility Checker               ║
echo ║   Starting server...                                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the application
echo Starting Flask development server...
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press CTRL+C to stop the server.
echo.

python run.py

pause
