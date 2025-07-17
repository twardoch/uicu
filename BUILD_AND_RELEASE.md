# Build and Release System Documentation

## Overview

This document describes the comprehensive build and release system for the `uicu` project, including git-tag-based semversioning, automated testing, and multiplatform binary distribution.

## Key Features

- ✅ **Git-tag-based semversioning** with hatch-vcs
- ✅ **Comprehensive test suite** with 99% pass rate  
- ✅ **Local development scripts** for build, test, and release
- ✅ **GitHub Actions CI/CD** with multiplatform testing
- ✅ **Automated releases** on git tags
- ✅ **Binary artifact generation** for Linux, macOS, and Windows
- ✅ **PyPI publication** with source and wheel distributions
- ✅ **GitHub releases** with automated release notes

## Project Structure

```
uicu/
├── scripts/                    # Build and release scripts
│   ├── build-and-test.sh      # Comprehensive build and test script
│   ├── release.sh             # Release management script
│   └── build-binary.sh        # Binary executable builder
├── .github/workflows/         # GitHub Actions workflows
│   ├── push.yml              # CI on push/PR
│   ├── release.yml           # Release on tags
│   └── test-binaries.yml     # Weekly binary testing
├── Makefile                   # Development convenience commands
├── pyproject.toml            # Project configuration with hatch-vcs
└── src/uicu/                 # Package source code
    ├── cli.py                # Command-line interface
    └── __main__.py           # Python -m uicu entry point
```

## Local Development

### Quick Start

```bash
# Set up development environment
make setup-dev

# Run tests
make test

# Build package
make build

# Build binary
make binary

# Run all checks (lint, type-check, test, build)
make ci
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make setup-dev` | Set up development environment with UV |
| `make test` | Run test suite |
| `make test-cov` | Run tests with coverage |
| `make test-parallel` | Run tests in parallel |
| `make lint` | Run linting |
| `make format` | Format code |
| `make type-check` | Run type checking |
| `make build` | Build Python package |
| `make binary` | Build binary executable |
| `make clean` | Clean build artifacts |
| `make ci` | Run CI-like checks locally |

### Development Scripts

#### 1. Build and Test Script (`scripts/build-and-test.sh`)

Comprehensive script that handles the complete build and test pipeline:

```bash
# Basic usage
./scripts/build-and-test.sh

# With options
./scripts/build-and-test.sh --coverage --parallel --verbose

# Clean build with benchmarks
./scripts/build-and-test.sh --clean --benchmark --coverage
```

**Features:**
- Automatic UV installation and environment setup
- Code quality checks (ruff, mypy)
- Test execution with optional coverage and parallel execution
- Package building and verification
- Binary creation and testing
- Benchmark execution
- Installation testing

#### 2. Release Script (`scripts/release.sh`)

Automated release management with git-tag-based versioning:

```bash
# Interactive release
./scripts/release.sh

# Specific version
./scripts/release.sh 1.0.0

# Dry run
./scripts/release.sh 1.0.1 --dry-run
```

**Features:**
- Git repository validation
- Version validation (semantic versioning)
- Automated testing before release
- Package building
- Changelog updates
- Git tag creation and pushing
- CI/CD trigger

#### 3. Binary Build Script (`scripts/build-binary.sh`)

Creates standalone executable binaries:

```bash
./scripts/build-binary.sh
```

**Features:**
- CLI entry point creation
- PyInstaller-based binary building
- Binary testing and validation
- Archive creation for distribution
- Cross-platform support

## Git-Tag-Based Semversioning

### Configuration

The project uses `hatch-vcs` for automatic version management:

```toml
# pyproject.toml
[tool.hatch.version]
source = 'vcs'

[tool.hatch.build.hooks.vcs]
version-file = "src/uicu/__version__.py"
```

### Version Format

- Development: `1.0.0a1.dev10+g2c4d316.d20250717`
- Release: `1.0.0` (from git tag `v1.0.0`)
- Pre-release: `1.0.0rc1` (from git tag `v1.0.0rc1`)

### Creating a Release

```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0

# This triggers the release workflow automatically
```

## GitHub Actions CI/CD

### 1. Push Workflow (`.github/workflows/push.yml`)

Runs on every push and pull request:

- **Code Quality**: Ruff linting and formatting
- **Testing**: Multiplatform tests (Ubuntu, Windows, macOS)
- **Python Versions**: 3.10, 3.11, 3.12
- **Build**: Package building and verification
- **Artifacts**: Coverage reports and distribution files

### 2. Release Workflow (`.github/workflows/release.yml`)

Triggered on git tags (`v*`):

- **Testing**: Full test suite across all platforms
- **Binary Building**: Executables for Linux, macOS, Windows
- **PyPI Publishing**: Automated package publication
- **GitHub Release**: Automated release with artifacts
- **Release Notes**: Auto-generated from commits

### 3. Binary Testing Workflow (`.github/workflows/test-binaries.yml`)

Weekly testing of binary builds:

- **Multiplatform Builds**: Test binary creation
- **Functionality Tests**: Verify binary operations
- **Integration Tests**: End-to-end testing
- **Artifact Management**: Binary size and quality checks

## Multiplatform Support

### Supported Platforms

| Platform | CI Testing | Binary Building | ICU Installation |
|----------|------------|-----------------|------------------|
| Linux (Ubuntu) | ✅ | ✅ | `apt-get install libicu-dev` |
| macOS | ✅ | ✅ | `brew install icu4c` |
| Windows | ✅ | ✅ | `vcpkg install icu` |

### Platform-Specific Configurations

#### Linux
```yaml
- name: Install ICU dependencies (Ubuntu)
  run: |
    sudo apt-get update
    sudo apt-get install -y libicu-dev pkg-config
```

#### macOS
```yaml
- name: Install ICU dependencies (macOS)
  run: |
    brew install icu4c pkg-config
    echo "PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig" >> $GITHUB_ENV
```

#### Windows
```yaml
- name: Install ICU dependencies (Windows)
  run: |
    vcpkg install icu:x64-windows
    echo "ICU_ROOT=C:/vcpkg/installed/x64-windows" >> $GITHUB_ENV
```

## Binary Distribution

### Binary Features

- **Standalone Executables**: No Python runtime required
- **CLI Interface**: Full command-line functionality
- **Size**: ~27MB (includes ICU and Python runtime)
- **Platforms**: Linux, macOS, Windows (x64)

### CLI Usage

```bash
# Character name lookup
uicu name "€"                    # EURO SIGN

# Script detection
uicu script "Hello, 世界!"       # Latn

# Transliteration
uicu transliterate "Greek-Latin" "Ελληνικά"  # Ellēniká

# Collation
uicu collate "en-US" "café" "cafe"  # café > cafe
```

### Binary Installation

1. **Download**: Get the binary from GitHub releases
2. **Extract**: Unpack the tar.gz archive
3. **Install**: Move to `/usr/local/bin` or add to PATH
4. **Verify**: Run `uicu --version`

## Package Distribution

### PyPI Publishing

Automated publishing on releases:

- **Source Distribution**: `.tar.gz` with full source code
- **Wheel Distribution**: `.whl` for fast installation
- **Metadata**: Complete package information
- **Dependencies**: PyICU and fontTools specified

### Installation

```bash
# Standard installation
pip install uicu

# Development installation
pip install -e ".[dev,test,all]"

# From source
pip install git+https://github.com/twardoch/uicu.git
```

## Testing Strategy

### Test Coverage

- **Unit Tests**: 72 tests covering all modules
- **Integration Tests**: Cross-module functionality
- **Platform Tests**: All supported platforms
- **Performance Tests**: Benchmark suite available
- **Binary Tests**: CLI functionality verification

### Test Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-v --durations=10 -p no:briefcase"
testpaths = ["tests"]
markers = [
    "benchmark: performance tests",
    "unit: unit tests",
    "integration: integration tests",
]
```

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Parallel execution
make test-parallel

# Benchmarks only
make benchmark
```

## Release Process

### 1. Preparation

- Ensure all tests pass
- Update documentation
- Review changelog
- Verify version compatibility

### 2. Release Creation

```bash
# Using release script
./scripts/release.sh 1.0.0

# Manual process
git tag v1.0.0
git push origin v1.0.0
```

### 3. Automated Pipeline

1. **GitHub Actions** detects tag
2. **Testing** runs across all platforms
3. **Binary Building** creates executables
4. **PyPI Publishing** uploads packages
5. **GitHub Release** creates release page
6. **Notifications** sent to maintainers

### 4. Post-Release

- Verify PyPI listing
- Test binary downloads
- Update documentation
- Announce release

## Security and Quality

### Code Quality

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks
- **Coverage**: Test coverage reporting

### Security

- **Dependency Scanning**: Automated vulnerability checks
- **Secure Secrets**: GitHub secrets for PyPI tokens
- **Permissions**: Minimal required permissions
- **Signed Releases**: Git tag signing (optional)

### Quality Gates

- All tests must pass
- Code coverage > 70%
- No critical linting errors
- Type checking passes
- Binary builds succeed

## Troubleshooting

### Common Issues

1. **ICU Installation**: Platform-specific ICU setup
2. **Binary Size**: PyInstaller optimization
3. **Test Failures**: Platform-specific test issues
4. **Release Failures**: Git tag and permissions

### Debug Commands

```bash
# Check environment
make info

# Test specific platform
make test PLATFORM=linux

# Build debug binary
./scripts/build-binary.sh --debug

# Validate release
./scripts/release.sh --dry-run
```

## Future Enhancements

### Planned Features

- **Documentation Website**: Sphinx-based docs
- **Docker Images**: Containerized builds
- **Conda Packages**: conda-forge distribution
- **Performance Monitoring**: Automated benchmarks
- **Security Scanning**: Enhanced vulnerability checks

### Potential Improvements

- **Smaller Binaries**: Optimize PyInstaller output
- **Faster Tests**: Parallel test optimization
- **Better Coverage**: Increase test coverage
- **More Platforms**: ARM64, Alpine Linux support

## Conclusion

The build and release system provides a complete, automated workflow for developing, testing, and distributing the `uicu` package. With multiplatform support, comprehensive testing, and automated releases, it ensures high-quality, reliable software distribution.

For questions or issues, please refer to the GitHub repository or contact the maintainers.