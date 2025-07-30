@echo off
REM ========================================
REM Demonling Game Launcher for Windows
REM This batch file automatically checks dependencies and runs the game
REM ========================================

echo Starting Demonling - Turn-Based RPG...
echo.

REM ========================================
REM Step 1: Check if Python is installed
REM ========================================
REM Try to run python --version and check if it succeeds
python --version >nul 2>&1
if errorlevel 1 (
    REM If python command fails, show error message
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1  REM Exit with error code 1
)

REM ========================================
REM Step 2: Test if all dependencies are installed
REM ========================================
echo Testing installation...
python test_installation.py
if errorlevel 1 (
    REM If test fails, try to install dependencies automatically
    echo.
    echo Installation test failed. Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Testing installation again...
    python test_installation.py
    if errorlevel 1 (
        REM If installation still fails, show error and exit
        echo.
        echo Failed to install dependencies. Please check your Python installation.
        pause
        exit /b 1
    )
)

REM ========================================
REM Step 3: Start the game
REM ========================================
echo.
echo Starting the game...
python main.py

REM Keep the window open so user can see any error messages
pause 