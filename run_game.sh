#!/bin/bash

# ========================================
# Demonling Game Launcher for Linux/Mac
# This shell script automatically checks dependencies and runs the game
# ========================================

echo "Starting Demonling - Turn-Based RPG..."
echo

# ========================================
# Step 1: Check if Python 3 is installed
# ========================================
# The 'command -v' command checks if a command exists in PATH
# '&> /dev/null' redirects both stdout and stderr to /dev/null (discards output)
if ! command -v python3 &> /dev/null; then
    # If python3 command is not found, show error message
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1  # Exit with error code 1
fi

# ========================================
# Step 2: Test if all dependencies are installed
# ========================================
echo "Testing installation..."
python3 test_installation.py
if [ $? -ne 0 ]; then
    # If test fails (exit code not 0), try to install dependencies automatically
    echo
    echo "Installation test failed. Installing dependencies..."
    pip3 install -r requirements.txt
    echo
    echo "Testing installation again..."
    python3 test_installation.py
    if [ $? -ne 0 ]; then
        # If installation still fails, show error and exit
        echo
        echo "Failed to install dependencies. Please check your Python installation."
        exit 1
    fi
fi

# ========================================
# Step 3: Start the game
# ========================================
echo
echo "Starting the game..."
python3 main.py 