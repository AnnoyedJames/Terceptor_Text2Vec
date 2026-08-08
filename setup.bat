@echo off
echo Setting up environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found. Install it from https://python.org and re-run this script.
    pause
    exit /b 1
)
echo Installing dependencies (this may take a few minutes)...
venv\Scripts\pip install -r requirements.txt
echo.
echo Place your comma-separated terms in input.txt
echo Like this: tag, tag, tag, tag
echo Then run:
echo   venv\Scripts\python.exe embed.py
pause
