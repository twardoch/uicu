#!/bin/bash
# this_file: build-docs.sh
# Build script for UICU documentation

echo "Building UICU Documentation"
echo "=========================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install documentation dependencies
echo "Installing documentation dependencies..."
pip install -r docs-requirements.txt

# Build the documentation
echo "Building documentation..."
mkdocs build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Documentation built successfully!"
    echo "Output is in the 'docs' directory"
else
    echo "Documentation build failed!"
    exit 1
fi

echo "Done!"