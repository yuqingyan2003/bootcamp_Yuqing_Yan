#!/bin/bash
# Startup script for AAPL Stock Prediction API

echo "Starting AAPL Stock Prediction API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "model/model.pkl" ]; then
    echo "Error: model.pkl not found. Please run the notebook first."
    exit 1
fi

# Start the API
echo "Starting Flask API on http://localhost:5000"
echo "Press Ctrl+C to stop"
python app.py
