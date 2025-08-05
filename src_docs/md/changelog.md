---
# this_file: src_docs/md/changelog.md
title: Changelog
description: UICU release history and changes
---

# Changelog

All notable changes to UICU will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation with 9 detailed chapters
- MkDocs Material theme documentation site
- GitHub Actions workflow for automatic documentation building
- Complete user guide covering all UICU features

### Changed
- Documentation structure reorganized for better navigation
- Improved examples throughout documentation

## [0.1.0] - 2024-01-XX

### Added
- Initial UICU package release
- Core Unicode character analysis with `Char` class
- Locale-aware text processing with `Locale` class
- Text collation support with `Collator` class
- Text segmentation capabilities
- Transliteration support for script conversion
- Date and time formatting
- Comprehensive test suite
- CLI interface for quick operations

### Technical Details
- Python 3.8+ support
- PyICU integration for core Unicode operations
- fontTools.unicodedata integration for extended Unicode data
- Type hints throughout the codebase
- Performance optimizations with caching
- 96KB package size with <100ms import time

## Development

### Contributing
See [Development Guide](development/index.md) for information about contributing to UICU.

### Release Process
1. Update version in `pyproject.toml`
2. Update this changelog
3. Create release tag
4. GitHub Actions handles PyPI publication

---

For the complete commit history, see the [GitHub repository](https://github.com/twardoch/uicu/commits/main).