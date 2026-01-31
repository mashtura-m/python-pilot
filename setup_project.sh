#!/bin/bash

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install system dependencies required to build lxml (libxml2, libxslt, etc.)
echo "Installing system dependencies for lxml..."
sudo apt-get install -y libxml2-dev libxslt1-dev python3-dev build-essential

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Check if the virtual environment's activate script exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment is not set up correctly. Please recreate it."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Ensure pip is up-to-date inside the virtual environment
echo "Upgrading pip inside virtual environment..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Virtual environment set up and dependencies installed!"
