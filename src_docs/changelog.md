# Changelog

All notable changes to UICU are documented here.

## [1.0.0] - 2025-01-26 (Upcoming)

### 🎉 Initial Release

UICU v1.0 delivers fast, reliable, essential Unicode operations with a Pythonic API.

### ✨ Features

#### Core Unicode Operations
- **Character Properties** - Complete Unicode character analysis with fontTools integration
  - Character names, categories, scripts, blocks
  - Bidirectional properties and mirroring
  - Numeric values and combining classes
  - Enhanced data from fontTools.unicodedata

#### Locale Management
- **BCP 47 Compliant** - Full locale handling with factory patterns
  - Parse and validate locale identifiers
  - Access language, script, region components
  - Display names in various languages
  - Factory methods for creating locale-specific services

#### Text Collation
- **Culture-Aware Sorting** - Locale-sensitive string comparison
  - Customizable strength levels (primary, secondary, tertiary)
  - Numeric sorting support
  - Case-first options
  - Efficient sort key generation

#### Text Segmentation
- **Unicode-Compliant Breaking** - Proper text boundary detection
  - Grapheme cluster segmentation (user-perceived characters)
  - Word boundary detection with locale awareness
  - Sentence segmentation with abbreviation handling
  - Line break opportunity detection

#### Script Transformation
- **Transliteration** - Powerful text transformation engine
  - Script-to-script conversion (Greek→Latin, Cyrillic→Latin, etc.)
  - Case transformation (upper, lower, title)
  - Accent removal and normalization
  - Custom transformation rules

#### Date/Time Formatting
- **Locale-Aware Formatting** - Cultural date/time representation
  - Multiple style options (short, medium, long, full)
  - Pattern-based formatting
  - Timezone support
  - Locale-specific conventions

### 🚀 Performance

- **Import Time**: 16.9ms (target: <100ms) ✅
- **Package Size**: 96KB source (target: <100KB) ✅
- **Code Size**: 2,418 lines (close to 2000 target)
- **Minimal Overhead**: Direct PyICU wrapping for maximum speed

### 🏗️ Architecture

- **Clean Modular Design** - Well-organized module structure
- **Consistent API** - Pythonic interfaces throughout
- **Type Safety** - Full type hints for better IDE support
- **Error Handling** - Clear, informative error messages

### 📦 Dependencies

- **Required**: PyICU ≥ 2.11
- **Optional**: fontTools[unicode] ≥ 4.38.0 (for enhanced features)
- **Python**: 3.10+ support

### 🧪 Quality

- **Test Coverage**: 73% overall, 88% for core modules
- **Test Suite**: 88 tests with comprehensive scenarios
- **Linting**: Minimal warnings, clean codebase
- **Documentation**: Complete API docs and examples

### 📚 Documentation

- Comprehensive README with quick start guide
- API documentation for all public interfaces
- Multiple real-world examples
- Contributing guidelines

### 🔧 Developer Experience

- **Hatch Integration** - Modern Python packaging
- **Development Tools** - Linting, formatting, type checking
- **CI/CD Ready** - GitHub Actions workflows
- **Cross-Platform** - Windows, macOS, Linux support

## [1.0.0-alpha] - 2025-01-25

### 🔬 Alpha Release

Pre-release version for testing and feedback.

### Features
- Initial implementation of all core modules
- Basic test suite
- Documentation structure

### Known Issues
- 8 test failures to be fixed for 1.0.0
- Minor formatting inconsistencies
- Some edge cases in date/time formatting

## Future Releases

### [2.0.0] - Planned Features

#### Number Formatting
- Decimal, currency, percent, scientific notation
- Locale-specific number systems
- Rounding and precision control

#### Message Formatting
- ICU MessageFormat support
- Plural rules and gender selection
- Complex message composition

#### Advanced Features
- Unicode regular expressions
- Relative time formatting ("3 days ago")
- Duration formatting
- Calendar calculations
- Advanced timezone handling

#### Developer Tools
- Sphinx documentation site
- Interactive playground
- Performance benchmarks
- Migration tools

## Version History

| Version | Date | Status | Highlights |
|---------|------|--------|------------|
| 1.0.0 | 2025-01-26 | Upcoming | Production-ready release |
| 1.0.0-alpha | 2025-01-25 | Released | Alpha testing version |
| 0.1.0 | 2025-01-20 | Development | Initial development |

## Deprecation Policy

UICU follows semantic versioning:

- **Major versions** (X.0.0) may include breaking changes
- **Minor versions** (1.X.0) add functionality in a backward-compatible manner
- **Patch versions** (1.0.X) make backward-compatible bug fixes

Deprecated features will:
1. Generate warnings for one minor version
2. Be documented in the changelog
3. Include migration instructions
4. Be removed in the next major version

## Upgrade Guide

### From Pre-1.0 to 1.0

No breaking changes are expected. The 1.0 release focuses on:
- Fixing remaining test failures
- Improving performance
- Enhancing documentation

Simply upgrade using:
```bash
pip install --upgrade uicu
```

## Release Notes Format

Each release includes:
- **Features** - New functionality added
- **Improvements** - Enhancements to existing features
- **Bug Fixes** - Resolved issues
- **Performance** - Speed or memory improvements
- **Documentation** - Doc updates and corrections
- **Dependencies** - Dependency changes
- **Deprecations** - Features marked for removal
- **Breaking Changes** - Incompatible changes (major versions only)