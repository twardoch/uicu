# Development

This section covers development practices, architecture, and contribution guidelines for UICU.

## Overview

UICU is built with modern Python development practices:
- **Type Safety**: Full type annotations throughout
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Enforced with ruff, black, and mypy
- **Packaging**: Modern packaging with hatch and uv
- **Documentation**: Auto-generated from docstrings

## Development Sections

<div class="grid cards" markdown>

-   :material-hand-heart:{ .lg .middle } **[Contributing](contributing.md)**

    ---

    How to contribute code, documentation, and bug reports to UICU

    [:octicons-arrow-right-24: Contribution guide](contributing.md)

-   :material-layers:{ .lg .middle } **[Architecture](architecture.md)**

    ---

    Understanding UICU's design, module structure, and ICU integration

    [:octicons-arrow-right-24: Architecture overview](architecture.md)

-   :material-test-tube:{ .lg .middle } **[Testing](testing.md)**

    ---

    Running tests, writing new tests, and maintaining test quality

    [:octicons-arrow-right-24: Testing guide](testing.md)

-   :material-hammer-wrench:{ .lg .middle } **[Building](building.md)**

    ---

    Building UICU from source, creating wheels, and packaging

    [:octicons-arrow-right-24: Build instructions](building.md)

-   :material-package-up:{ .lg .middle } **[Releasing](releasing.md)**

    ---

    Release process, versioning, and distribution procedures

    [:octicons-arrow-right-24: Release guide](releasing.md)

</div>

## Quick Start for Developers

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/twardoch/uicu.git
cd uicu

# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv --python 3.12

# Install in development mode
uv pip install -e ".[dev]"

# Or use hatch
hatch shell
```

### Running Tests

```bash
# Run all tests
hatch run test

# Run with coverage
hatch run test-cov

# Run specific test file
python -m pytest tests/test_char.py -v

# Run with different Python version
hatch run test-py311
```

### Code Quality Checks

```bash
# Run linting
hatch run lint

# Format code
hatch run format

# Type checking
hatch run type-check

# All checks
hatch run all
```

### Making Changes

1. **Create a branch**: `git checkout -b feature/your-feature`
2. **Make changes**: Edit code and add tests
3. **Run tests**: `hatch run test`
4. **Check quality**: `hatch run lint`
5. **Commit**: `git commit -m "feat: add new feature"`
6. **Push**: `git push origin feature/your-feature`
7. **Open PR**: Create pull request on GitHub

## Project Structure

```
uicu/
├── src/uicu/          # Source code
│   ├── __init__.py    # Package exports
│   ├── char.py        # Character properties
│   ├── locale.py      # Locale management
│   ├── collate.py     # Text collation
│   ├── segment.py     # Text segmentation
│   ├── translit.py    # Transliteration
│   ├── format.py      # Date/time formatting
│   ├── exceptions.py  # Exception classes
│   └── _utils.py      # Internal utilities
├── tests/             # Test suite
│   ├── test_char.py
│   ├── test_locale.py
│   └── ...
├── docs/              # Built documentation
├── src_docs/          # Documentation source
├── examples/          # Example scripts
├── pyproject.toml     # Project configuration
└── Makefile          # Development shortcuts
```

## Development Tools

### uv (Recommended)
Fast, modern Python package installer:
```bash
# Install packages
uv pip install package-name

# Sync dependencies
uv pip sync requirements.txt

# Create virtual environment
uv venv
```

### Hatch
Build backend and development workflow:
```bash
# Enter development shell
hatch shell

# Run commands in environment
hatch run test
hatch run lint
```

### pytest
Testing framework with rich features:
```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_char.py::TestChar::test_basic_properties

# Run with debugging
pytest --pdb
```

### Ruff
Fast Python linter and formatter:
```bash
# Check code
ruff check src/

# Fix issues
ruff check --fix src/

# Format code
ruff format src/
```

## Code Style

UICU follows these conventions:
- **PEP 8** compliant (enforced by ruff)
- **Black** formatting style
- **Google-style** docstrings
- **Type annotations** required for public APIs
- **f-strings** for formatting
- **Path objects** over string paths

Example:
```python
from pathlib import Path
from typing import Optional

def process_file(path: Path, encoding: str = "utf-8") -> Optional[str]:
    """Process a file and return its contents.
    
    Args:
        path: Path to the file to process.
        encoding: File encoding (default: utf-8).
        
    Returns:
        File contents as string, or None if file doesn't exist.
        
    Raises:
        UICUError: If file cannot be decoded.
    """
    if not path.exists():
        return None
        
    try:
        return path.read_text(encoding=encoding)
    except UnicodeDecodeError as e:
        raise UICUError(f"Cannot decode {path}: {e}") from e
```

## Performance Guidelines

1. **Cache Expensive Objects**: ICU objects are expensive to create
2. **Batch Operations**: Process multiple items together
3. **Profile First**: Measure before optimizing
4. **Memory Awareness**: ICU objects can be memory-intensive

## Documentation Standards

- **Docstrings**: Required for all public APIs
- **Type Hints**: Required for all public functions
- **Examples**: Include in docstrings where helpful
- **Cross-References**: Link related functionality

## Next Steps

- Read [Contributing](contributing.md) for contribution guidelines
- Study [Architecture](architecture.md) to understand the design
- Check [Testing](testing.md) for test practices
- See [Building](building.md) for build instructions