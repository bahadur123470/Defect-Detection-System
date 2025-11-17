#!/bin/bash
# Quick start script for the Defect Detection System

echo "Starting Defect Detection System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads static/processed reports models

# Start the application
echo ""
echo "Starting Flask application..."
echo "Open your browser and navigate to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py

