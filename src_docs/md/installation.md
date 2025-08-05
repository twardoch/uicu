---
# this_file: src_docs/md/installation.md
title: Installation Guide
description: Detailed setup instructions for all platforms
---

# Installation Guide

This guide covers installing UICU on different platforms and resolving common setup issues.

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 100MB+ available RAM
- **Disk Space**: 50MB for package and dependencies

## Quick Installation

For most users, pip installation is sufficient:

```bash
pip install uicu
```

This automatically installs PyICU and other required dependencies.

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian

Install ICU development libraries first:

```bash
# Install ICU libraries
sudo apt-get update
sudo apt-get install libicu-dev

# Install UICU
pip install uicu
```

#### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL
sudo yum install libicu-devel
# or for newer versions:
sudo dnf install libicu-devel

# Fedora
sudo dnf install libicu-devel

# Install UICU
pip install uicu
```

#### Alpine Linux

```bash
# Install ICU development package
sudo apk add icu-dev

# Install UICU
pip install uicu
```

### macOS

#### Using Homebrew (Recommended)

```bash
# Install ICU via Homebrew
brew install icu4c

# Set environment variables for PyICU compilation
export PATH="/opt/homebrew/bin:$PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"

# Install UICU
pip install uicu
```

#### Using MacPorts

```bash
# Install ICU via MacPorts
sudo port install icu

# Set environment variables
export PATH="/opt/local/bin:$PATH"
export PKG_CONFIG_PATH="/opt/local/lib/pkgconfig"

# Install UICU
pip install uicu
```

### Windows

#### Using conda (Recommended)

```bash
# Install with conda (includes ICU automatically)
conda install -c conda-forge pyicu
pip install uicu
```

#### Using pip with pre-built wheels

```bash
# This usually works on most Windows systems
pip install uicu
```

#### Manual ICU Installation

If pip fails, install ICU manually:

1. Download ICU binaries from [ICU releases](https://github.com/unicode-org/icu/releases)
2. Extract to `C:\icu`
3. Set environment variables:
   ```cmd
   set ICU_ROOT=C:\icu
   set PATH=%PATH%;C:\icu\bin64
   ```
4. Install UICU:
   ```bash
   pip install uicu
   ```

## Virtual Environments

### Using venv

```bash
# Create virtual environment
python -m venv uicu-env

# Activate (Linux/macOS)
source uicu-env/bin/activate

# Activate (Windows)
uicu-env\Scripts\activate

# Install UICU
pip install uicu
```

### Using conda

```bash
# Create conda environment
conda create -n uicu-env python=3.11

# Activate environment
conda activate uicu-env

# Install with conda-forge channel
conda install -c conda-forge pyicu
pip install uicu
```

### Using Poetry

```bash
# Initialize project (if not exists)
poetry init

# Add UICU dependency
poetry add uicu

# Install dependencies
poetry install

# Activate shell
poetry shell
```

## Development Installation

For development or contributing to UICU:

```bash
# Clone repository
git clone https://github.com/twardoch/uicu.git
cd uicu

# Install in development mode
pip install -e ".[dev]"

# Or with all optional dependencies
pip install -e ".[dev,test,docs]"
```

## Verification

Verify your installation:

```python
import uicu
print(f"UICU version: {uicu.__version__}")

# Test basic functionality
char = uicu.Char('A')
print(f"Character info: {char.name} ({char.category})")

# Test PyICU integration
locale = uicu.Locale('en-US')
print(f"Locale: {locale.display_name}")
```

Expected output:
```
UICU version: 0.1.0
Character info: LATIN CAPITAL LETTER A (Lu)
Locale: English (United States)
```

## Troubleshooting

### Common Issues

#### "PyICU compilation failed"

**Solution**: Install ICU development libraries for your platform (see platform-specific instructions above).

#### "ICU library not found"

**Linux/macOS Solution**:
```bash
# Find ICU installation
pkg-config --modversion icu-uc
pkg-config --cflags --libs icu-uc

# Set environment variables if needed
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
```

**Windows Solution**:
```cmd
# Ensure ICU is in PATH
echo %PATH%
# Should include ICU bin directory
```

#### "ImportError: No module named '_icu'"

This indicates PyICU installation failed. Try:

```bash
# Reinstall PyICU explicitly
pip uninstall PyICU
pip install --no-cache-dir PyICU

# Then reinstall UICU
pip install --force-reinstall uicu
```

#### "UnicodeDecodeError" on import

This can occur with locale issues:

```bash
# Set UTF-8 locale (Linux/macOS)
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Windows: Use UTF-8 code page
chcp 65001
```

### Version Compatibility

| UICU Version | Python Version | PyICU Version | ICU Version |
|--------------|----------------|---------------|-------------|
| 0.1.x        | 3.8+           | 2.11+         | 71+         |
| 0.2.x        | 3.9+           | 2.12+         | 72+         |

### Performance Optimization

#### Caching ICU Data

Set environment variable to cache ICU data:

```bash
# Linux/macOS
export ICU_DATA_CACHE_SIZE=10485760  # 10MB cache

# Windows
set ICU_DATA_CACHE_SIZE=10485760
```

#### Memory Usage

Monitor memory usage for large text processing:

```python
import uicu
import psutil
import os

# Check memory before
process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / 1024 / 1024

# Process large text
large_text = "A" * 1000000
chars = [uicu.Char(c) for c in large_text[:1000]]  # Sample first 1000

# Check memory after
memory_after = process.memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_after - memory_before:.1f} MB")
```

## Docker Installation

For containerized applications:

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Install ICU libraries
RUN apt-get update && apt-get install -y \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UICU
RUN pip install uicu

# Verify installation
RUN python -c "import uicu; print('UICU installed successfully')"
```

## Alternative Installations

### From Source

```bash
# Download source
wget https://github.com/twardoch/uicu/archive/main.zip
unzip main.zip
cd uicu-main

# Build and install
python setup.py build
python setup.py install
```

### Development Snapshot

```bash
# Install latest development version
pip install git+https://github.com/twardoch/uicu.git
```

## Uninstallation

To completely remove UICU:

```bash
# Uninstall UICU
pip uninstall uicu

# Optionally remove PyICU (if not used by other packages)
pip uninstall PyICU
```

## Getting Help

If you encounter installation issues:

1. **Check the [Troubleshooting](#troubleshooting) section above**
2. **Search [GitHub Issues](https://github.com/twardoch/uicu/issues)**
3. **Create a new issue** with:
   - Your operating system and version
   - Python version (`python --version`)
   - Complete error message
   - Output of `pip list | grep -i icu`

## Next Steps

After successful installation:

1. **[Getting Started](getting-started.md)** - Your first UICU operations
2. **[Unicode Basics](guide/unicode-basics.md)** - Understanding Unicode fundamentals
3. **[Examples](examples/index.md)** - Real-world usage examples

!!! success "Installation Complete"
    You're ready to start using UICU! Try the [Getting Started](getting-started.md) guide for your first Unicode operations.