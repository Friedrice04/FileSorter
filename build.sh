#!/bin/bash
# Quick build script for Unix/Linux/Mac systems

echo "🚀 FileSorter Quick Build"
echo "========================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python not found. Please install Python 3.7+."
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "🐍 Using: $PYTHON_CMD"

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

# Run the build
echo "🏗️  Building executable..."
$PYTHON_CMD build.py

echo "✅ Build complete! Check the 'release' folder for your executable."
