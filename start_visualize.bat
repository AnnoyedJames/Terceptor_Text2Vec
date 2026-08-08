@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if errorlevel 1 exit /b 1
)

"%PYTHON%" -c "import numpy, plotly, umap" >nul 2>&1
if errorlevel 1 (
    echo Visualization dependencies are missing. Installing them...
    "%PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

"%PYTHON%" visualize.py
if errorlevel 1 pause
