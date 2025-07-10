#!/bin/bash

# Ernie's Adventure - Game Launcher Script
# This script automatically activates the virtual environment and runs the game

echo "🎮 Starting Ernie's Adventure..."
echo "📂 Project directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Make sure you're in the Ernie project directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "ernie_env" ]; then
    echo "❌ Error: Virtual environment 'ernie_env' not found."
    echo "💡 Run: python3 -m venv ernie_env && source ernie_env/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ernie_env/bin/activate

# Check if pygame is installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "❌ Error: pygame not found in virtual environment."
    echo "🔧 Installing pygame..."
    pip install -r requirements.txt
fi

# Run the game with all passed arguments
echo "🚀 Launching game..."
echo ""
python3 main.py "$@" 