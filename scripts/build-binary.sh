#!/bin/bash
# this_file: scripts/build-binary.sh
# Binary build script for uicu project
# Usage: ./scripts/build-binary.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    print_error "Must be run from project root directory"
    exit 1
fi

# Install UV if not present
if ! command -v uv &> /dev/null; then
    print_header "Installing UV package manager"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

# Create virtual environment if it doesn't exist
if [[ ! -d ".venv" ]]; then
    print_header "Creating virtual environment"
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies including PyInstaller
print_header "Installing binary build dependencies"
uv pip install -e ".[dev,test,all]"
uv pip install pyinstaller

# Create a CLI entry point if it doesn't exist
CLI_SCRIPT="src/uicu/cli.py"
if [[ ! -f "$CLI_SCRIPT" ]]; then
    print_header "Creating CLI entry point"
    cat > "$CLI_SCRIPT" << 'EOF'
#!/usr/bin/env python3
"""
CLI tool for uicu package.
"""
import sys
import argparse
from typing import Optional

import uicu


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="uicu - Unicode and ICU utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uicu script text "Hello, 世界!"
  uicu name "€"
  uicu transliterate "Greek-Latin" "Ελληνικά"
  uicu collate "en-US" "café" "cafe"
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"uicu {uicu.__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Script detection command
    script_parser = subparsers.add_parser("script", help="Detect script of text")
    script_parser.add_argument("text", help="Text to analyze")
    
    # Character name command
    name_parser = subparsers.add_parser("name", help="Get character name")
    name_parser.add_argument("char", help="Character to analyze")
    
    # Transliteration command
    translit_parser = subparsers.add_parser("transliterate", help="Transliterate text")
    translit_parser.add_argument("transform", help="Transform to apply")
    translit_parser.add_argument("text", help="Text to transliterate")
    
    # Collation command
    collate_parser = subparsers.add_parser("collate", help="Compare strings")
    collate_parser.add_argument("locale", help="Locale to use")
    collate_parser.add_argument("text1", help="First text")
    collate_parser.add_argument("text2", help="Second text")
    
    args = parser.parse_args()
    
    try:
        if args.command == "script":
            result = uicu.detect_script(args.text)
            print(result if result else "Unknown")
        
        elif args.command == "name":
            if len(args.char) != 1:
                print("Error: Please provide a single character", file=sys.stderr)
                sys.exit(1)
            result = uicu.name(args.char)
            print(result)
        
        elif args.command == "transliterate":
            transliterator = uicu.Transliterator(args.transform)
            result = transliterator.transliterate(args.text)
            print(result)
        
        elif args.command == "collate":
            collator = uicu.Collator(args.locale)
            result = collator.compare(args.text1, args.text2)
            if result == 0:
                print("Equal")
            elif result < 0:
                print(f"'{args.text1}' < '{args.text2}'")
            else:
                print(f"'{args.text1}' > '{args.text2}'")
        
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
EOF
    print_success "CLI entry point created"
fi

# Build binary with PyInstaller
print_header "Building binary with PyInstaller"

# Create build directory
mkdir -p build/binary

# Build the binary
uv run pyinstaller \
    --onefile \
    --name uicu \
    --distpath build/binary \
    --workpath build/binary/work \
    --specpath build/binary \
    --clean \
    --console \
    src/uicu/cli.py

# Test the binary
print_header "Testing binary"
BINARY_PATH="build/binary/uicu"
if [[ -f "$BINARY_PATH" ]]; then
    echo "Binary size: $(du -h $BINARY_PATH | cut -f1)"
    echo "Binary info:"
    file "$BINARY_PATH"
    echo ""
    echo "Testing binary:"
    "$BINARY_PATH" --version
    "$BINARY_PATH" --help
    print_success "Binary built and tested successfully"
else
    print_error "Binary not found at $BINARY_PATH"
    exit 1
fi

# Create archive
print_header "Creating distribution archive"
cd build/binary
tar -czf uicu-binary-$(uname -s)-$(uname -m).tar.gz uicu
ls -la uicu-binary-*.tar.gz
cd - > /dev/null

print_success "Binary build completed!"
echo "Binary location: $BINARY_PATH"
echo "Archive location: build/binary/uicu-binary-$(uname -s)-$(uname -m).tar.gz"