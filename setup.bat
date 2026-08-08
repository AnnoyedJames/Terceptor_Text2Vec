@echo off
echo Setting up environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found. Install it from https://python.org and re-run this script.
    pause
    exit /b 1
)
echo Installing PyTorch with CUDA 12.4 support...
venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cu124
echo Installing remaining dependencies...
venv\Scripts\pip install -r requirements.txt
echo.
echo Done! Place your comma-separated terms in input.txt, then run:
echo   venv\Scripts\python.exe embed.py
pause
