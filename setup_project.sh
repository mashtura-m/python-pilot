#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install system dependencies required to build lxml (libxml2, libxslt, etc.)
echo "Installing system dependencies for lxml..."
sudo apt-get install -y libxml2-dev libxslt1-dev python3-dev build-essential

# Ensure pip is up-to-date
echo "Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel



# Install the Python dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt


