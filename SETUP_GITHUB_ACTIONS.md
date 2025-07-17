# GitHub Actions Setup Guide

## Overview

This guide explains how to set up the complete CI/CD pipeline for the uicu project, including git-tag-based releases and multiplatform binary distribution.

## Files to Update

The following GitHub Actions workflow files need to be updated manually due to permissions restrictions:

### 1. `.github/workflows/push.yml` - Enhanced CI Pipeline

Replace the contents of `.github/workflows/push.yml` with the enhanced version that includes:
- Multiplatform testing (Ubuntu, macOS, Windows)
- ICU dependency installation per platform
- Coverage reporting optimization

### 2. `.github/workflows/release.yml` - Complete Release Pipeline

Replace the contents of `.github/workflows/release.yml` with the enhanced version that includes:
- Multiplatform testing before release
- Binary artifact generation
- PyPI publishing
- GitHub release creation with binaries

### 3. `.github/workflows/test-binaries.yml` - Binary Testing (New File)

Create a new file `.github/workflows/test-binaries.yml` for weekly binary testing.

## Enhanced Workflow Files

### 1. Enhanced Push Workflow

```yaml
name: Build & Test

on:
  push:
    branches: [main]
    tags-ignore: ["v*"]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  id-token: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Ruff lint
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "check --output-format=github"

      - name: Run Ruff Format
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "format --check --respect-gitignore"

  test:
    name: Run Tests
    needs: quality
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]
      fail-fast: false
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true
          cache-suffix: ${{ matrix.os }}-${{ matrix.python-version }}

      - name: Install ICU dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libicu-dev pkg-config

      - name: Install ICU dependencies (macOS)
        if: matrix.os == 'macos-latest'
        run: |
          brew install icu4c pkg-config
          echo "PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig" >> $GITHUB_ENV

      - name: Install ICU dependencies (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          # Use vcpkg to install ICU on Windows
          vcpkg install icu:x64-windows
          echo "ICU_ROOT=C:/vcpkg/installed/x64-windows" >> $GITHUB_ENV

      - name: Install test dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[test]"

      - name: Run tests with Pytest
        run: uv run pytest -n auto --maxfail=1 --disable-warnings --cov-report=xml --cov-config=pyproject.toml --cov=src/uicu --cov=tests tests/

      - name: Upload coverage report
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  build:
    name: Build Distribution
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install build tools
        run: uv pip install build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Upload distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-files
          path: dist/
          retention-days: 5
```

### 2. Enhanced Release Workflow

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write
  id-token: write

jobs:
  test:
    name: Run Tests
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]
      fail-fast: false
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Install ICU dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libicu-dev pkg-config

      - name: Install ICU dependencies (macOS)
        if: matrix.os == 'macos-latest'
        run: |
          brew install icu4c pkg-config
          echo "PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig" >> $GITHUB_ENV

      - name: Install ICU dependencies (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          vcpkg install icu:x64-windows
          echo "ICU_ROOT=C:/vcpkg/installed/x64-windows" >> $GITHUB_ENV

      - name: Install test dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[test]"

      - name: Run tests
        run: uv run pytest -n auto --maxfail=1 --disable-warnings tests/

  build-binaries:
    name: Build Binaries
    needs: test
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install ICU dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libicu-dev pkg-config

      - name: Install ICU dependencies (macOS)
        if: matrix.os == 'macos-latest'
        run: |
          brew install icu4c pkg-config
          echo "PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig" >> $GITHUB_ENV

      - name: Install ICU dependencies (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          vcpkg install icu:x64-windows
          echo "ICU_ROOT=C:/vcpkg/installed/x64-windows" >> $GITHUB_ENV

      - name: Install dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[dev,test,all]"
          uv pip install --system pyinstaller

      - name: Build binary
        run: |
          chmod +x scripts/build-binary.sh
          ./scripts/build-binary.sh
        shell: bash

      - name: Upload binary artifacts
        uses: actions/upload-artifact@v4
        with:
          name: binary-${{ matrix.os }}
          path: build/binary/uicu-binary-*.tar.gz

  release:
    name: Release to PyPI
    needs: [test, build-binaries]
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/uicu
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install ICU dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libicu-dev pkg-config

      - name: Install build tools
        run: uv pip install --system build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Verify distribution files
        run: |
          ls -la dist/
          test -n "$(find dist -name '*.whl')" || (echo "Wheel file missing" && exit 1)
          test -n "$(find dist -name '*.tar.gz')" || (echo "Source distribution missing" && exit 1)

      - name: Download binary artifacts
        uses: actions/download-artifact@v4
        with:
          path: binaries/

      - name: Prepare release assets
        run: |
          mkdir -p release-assets
          cp dist/* release-assets/
          find binaries/ -name "*.tar.gz" -exec cp {} release-assets/ \;
          ls -la release-assets/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: release-assets/*
          generate_release_notes: true
          body: |
            ## Release Notes
            
            This release includes:
            - Python wheels for multiple platforms
            - Source distribution
            - Compiled binaries for Linux, macOS, and Windows
            
            ## Installation
            
            ### Python Package
            ```bash
            pip install uicu
            ```
            
            ### Binary Installation
            Download the appropriate binary for your platform from the assets below.
            
            ## What's Changed
            See the full changelog and commit history below.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 3. Binary Testing Workflow (New File)

Create `.github/workflows/test-binaries.yml`:

```yaml
name: Test Binaries

on:
  workflow_dispatch:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM UTC

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test-binary-build:
    name: Test Binary Build
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Install ICU dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libicu-dev pkg-config

      - name: Install ICU dependencies (macOS)
        if: matrix.os == 'macos-latest'
        run: |
          brew install icu4c pkg-config
          echo "PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig" >> $GITHUB_ENV

      - name: Install ICU dependencies (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          vcpkg install icu:x64-windows
          echo "ICU_ROOT=C:/vcpkg/installed/x64-windows" >> $GITHUB_ENV

      - name: Install dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[dev,test,all]"
          uv pip install --system pyinstaller

      - name: Build binary
        run: |
          chmod +x scripts/build-binary.sh
          ./scripts/build-binary.sh
        shell: bash

      - name: Test binary functionality
        run: |
          # Test basic functionality
          ./build/binary/uicu --version
          ./build/binary/uicu --help
          
          # Test specific commands
          ./build/binary/uicu name "A"
          ./build/binary/uicu script "Hello"
          ./build/binary/uicu transliterate "Upper" "hello"
          ./build/binary/uicu collate "en-US" "a" "b"
        shell: bash

      - name: Upload binary for testing
        uses: actions/upload-artifact@v4
        with:
          name: test-binary-${{ matrix.os }}
          path: build/binary/uicu-binary-*.tar.gz
          retention-days: 7

  integration-test:
    name: Integration Test
    needs: test-binary-build
    runs-on: ubuntu-latest
    steps:
      - name: Download all binaries
        uses: actions/download-artifact@v4
        with:
          path: binaries/

      - name: Test binary downloads
        run: |
          echo "Downloaded binaries:"
          find binaries/ -name "*.tar.gz" -exec ls -la {} \;
          
          echo "Testing binary extraction:"
          for binary in binaries/*/uicu-binary-*.tar.gz; do
            echo "Testing: $binary"
            tar -tf "$binary" | head -5
          done

      - name: Verify binary sizes
        run: |
          echo "Binary sizes:"
          find binaries/ -name "*.tar.gz" -exec du -h {} \;
          
          # Check if binaries are not too large (>100MB might be problematic)
          for binary in binaries/*/uicu-binary-*.tar.gz; do
            size=$(du -m "$binary" | cut -f1)
            echo "Binary $binary size: ${size}MB"
            if [ "$size" -gt 100 ]; then
              echo "Warning: Binary $binary is larger than 100MB"
            fi
          done
```

## Repository Secrets Setup

### Required Secrets

1. **PYPI_TOKEN**: For automated PyPI publishing
   - Go to Settings → Secrets and variables → Actions
   - Add secret named `PYPI_TOKEN`
   - Value: Your PyPI API token

### Optional Secrets

1. **GITHUB_TOKEN**: Automatically provided by GitHub Actions
   - No setup required

## Setup Instructions

### 1. Update Existing Workflows

1. Navigate to your repository
2. Edit `.github/workflows/push.yml` and replace with the enhanced version above
3. Edit `.github/workflows/release.yml` and replace with the enhanced version above

### 2. Add New Workflow

1. Create `.github/workflows/test-binaries.yml` with the content above

### 3. Configure Repository Settings

1. **Enable Actions**: Go to Settings → Actions → General
2. **Allow Actions**: Set to "Allow all actions and reusable workflows"
3. **Workflow permissions**: Set to "Read and write permissions"

### 4. Set Up PyPI Publishing

1. Create PyPI account if you don't have one
2. Generate API token at https://pypi.org/manage/account/
3. Add `PYPI_TOKEN` secret to your repository

### 5. Test the Setup

1. **Test CI**: Create a pull request to test the enhanced CI
2. **Test Release**: Create a git tag to test the release process
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

## Features Enabled

### ✅ Multiplatform Testing
- Ubuntu, macOS, Windows
- Python 3.10, 3.11, 3.12
- ICU dependencies per platform

### ✅ Automated Releases
- Git-tag triggered releases
- PyPI publishing
- Binary generation
- GitHub releases with assets

### ✅ Quality Assurance
- Code formatting checks
- Comprehensive testing
- Binary functionality testing
- Weekly binary validation

### ✅ Artifact Management
- Python wheels and source distributions
- Platform-specific binaries
- Automated release notes
- Download links and installation instructions

## Troubleshooting

### Common Issues

1. **ICU Dependencies**: Platform-specific installation issues
2. **Binary Building**: PyInstaller compatibility
3. **Token Permissions**: PyPI publishing failures
4. **Workflow Permissions**: GitHub Actions restrictions

### Debug Steps

1. Check Actions tab for workflow runs
2. Review job logs for specific errors
3. Test locally with build scripts
4. Verify repository secrets and permissions

## Next Steps

After setting up the workflows:

1. **Test the CI**: Create a pull request to verify testing
2. **Test Release**: Create a test tag to verify release process
3. **Monitor**: Check Actions tab for successful runs
4. **Iterate**: Adjust workflows based on specific needs

The complete system provides automated testing, building, and releasing with multiplatform support and comprehensive artifact generation.