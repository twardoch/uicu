# Installation Guide

This guide covers all installation methods and troubleshooting tips for UICU.

## Requirements

### Python Version
- **Minimum**: Python 3.10
- **Recommended**: Python 3.11 or 3.12
- **Tested on**: Python 3.10, 3.11, 3.12

### Dependencies
- **PyICU** ≥ 2.11 (required)
- **fontTools[unicode]** ≥ 4.38.0 (optional, for enhanced Unicode data)

### System Requirements
- **Operating Systems**: Windows, macOS, Linux
- **Architecture**: x86_64, ARM64
- **Memory**: 100MB minimum
- **Disk Space**: 50MB for UICU + dependencies

## Installation Methods

### Standard Installation (pip)

The simplest way to install UICU:

```bash
pip install uicu
```

This will:
1. Download UICU from PyPI
2. Install PyICU (if not already installed)
3. Optionally install fontTools for enhanced features

### Installation with uv

For faster installation using [uv](https://github.com/astral-sh/uv):

```bash
uv pip install uicu
```

### Installation with Optional Dependencies

To ensure all optional features are available:

```bash
pip install "uicu[all]"
```

This includes:
- fontTools for enhanced Unicode data
- Additional script information
- Writing system detection

### Development Installation

For contributing or testing latest changes:

```bash
# Clone the repository
git clone https://github.com/twardoch/uicu.git
cd uicu

# Install in development mode
pip install -e ".[dev]"

# Or using hatch
hatch shell
```

### Installing from Source

To build from source:

```bash
# Clone the repository
git clone https://github.com/twardoch/uicu.git
cd uicu

# Build and install
python -m build
pip install dist/*.whl
```

## Platform-Specific Instructions

### macOS

=== "Homebrew"

    ```bash
    # Install ICU library
    brew install icu4c
    
    # Install PyICU with proper linking
    export PATH="/usr/local/opt/icu4c/bin:$PATH"
    export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"
    
    # Install UICU
    pip install uicu
    ```

=== "MacPorts"

    ```bash
    # Install ICU library
    sudo port install icu
    
    # Install UICU
    pip install uicu
    ```

### Linux

=== "Ubuntu/Debian"

    ```bash
    # Install system dependencies
    sudo apt-get update
    sudo apt-get install python3-dev libicu-dev
    
    # Install UICU
    pip install uicu
    ```

=== "Fedora/RHEL"

    ```bash
    # Install system dependencies
    sudo dnf install python3-devel libicu-devel
    
    # Install UICU
    pip install uicu
    ```

=== "Alpine"

    ```bash
    # Install system dependencies
    apk add python3-dev icu-dev g++
    
    # Install UICU
    pip install uicu
    ```

### Windows

=== "Pre-built Wheels"

    ```bash
    # PyICU provides pre-built wheels for Windows
    pip install uicu
    ```

=== "From Source"

    ```bash
    # Install Visual Studio Build Tools
    # Download from: https://visualstudio.microsoft.com/downloads/
    
    # Install ICU library (using vcpkg)
    vcpkg install icu
    
    # Set environment variables
    set ICU_ROOT=C:\vcpkg\installed\x64-windows
    
    # Install UICU
    pip install uicu
    ```

## Troubleshooting

### Common Issues

#### PyICU Installation Fails

**Problem**: `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution**: Install Visual Studio Build Tools
```bash
# Download and install from:
# https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
```

#### ICU Library Not Found

**Problem**: `error: ICU library not found`

**Solution**: Install ICU library for your platform
```bash
# macOS
brew install icu4c

# Ubuntu/Debian
sudo apt-get install libicu-dev

# Fedora
sudo dnf install libicu-devel
```

#### Import Error After Installation

**Problem**: `ImportError: cannot import name 'Char' from 'uicu'`

**Solution**: Ensure proper installation
```bash
# Uninstall and reinstall
pip uninstall uicu pyicu
pip install --no-cache-dir uicu
```

### Verifying Installation

After installation, verify everything works:

```python
# Test basic import
import uicu
print(f"UICU version: {uicu.__version__}")

# Test PyICU
import icu
print(f"ICU version: {icu.ICU_VERSION}")

# Test core functionality
char = uicu.Char('A')
print(f"Character name: {char.name}")

# Test optional features
try:
    from fontTools.unicodedata import script
    print("fontTools support: ✓")
except ImportError:
    print("fontTools support: ✗ (install with: pip install fontTools[unicode])")
```

### Environment Setup

For development work:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
pip install hatch

# Run tests
hatch run test

# Run linting
hatch run lint
```

## Docker Installation

For containerized environments:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libicu-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install UICU
RUN pip install uicu

# Verify installation
RUN python -c "import uicu; print(f'UICU {uicu.__version__} installed')"
```

## Conda Installation

For Anaconda/Miniconda users:

```bash
# Create new environment
conda create -n uicu-env python=3.11

# Activate environment
conda activate uicu-env

# Install PyICU from conda-forge
conda install -c conda-forge pyicu

# Install UICU
pip install uicu
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test UICU
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install system dependencies (Ubuntu)
      if: runner.os == 'Linux'
      run: |
        sudo apt-get update
        sudo apt-get install -y libicu-dev
    
    - name: Install system dependencies (macOS)
      if: runner.os == 'macOS'
      run: brew install icu4c
    
    - name: Install UICU
      run: pip install uicu
    
    - name: Test import
      run: python -c "import uicu; print(uicu.__version__)"
```

## Next Steps

After successful installation:

1. **[Get Started](getting-started.md)** - Learn the basics
2. **[API Reference](api/index.md)** - Explore the full API
3. **[Examples](examples/index.md)** - See UICU in action

## Getting Help

If you encounter issues:

1. Check the [troubleshooting](#troubleshooting) section above
2. Search [existing issues](https://github.com/twardoch/uicu/issues)
3. Ask on [GitHub Discussions](https://github.com/twardoch/uicu/discussions)
4. Report new issues with:
   - Python version
   - Operating system
   - Error messages
   - Installation method used