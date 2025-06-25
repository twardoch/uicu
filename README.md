# `uicu`

A Pythonic wrapper around PyICU with supplementary Unicode functionality from fontTools.unicodedata.

<!-- badges-begin -->
[![PyPI - Version](https://img.shields.io/pypi/v/uicu.svg)](https://pypi.org/project/uicu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uicu.svg)](https://pypi.org/project/uicu)
<!-- badges-end -->

## Overview

`uicu` provides natural, Pythonic interfaces to ICU's powerful internationalization and Unicode capabilities. It transforms PyICU's C++-style API into idiomatic Python, making advanced text processing accessible to Python developers.

### Key Features

- **Unicode Character Properties**: Rich character information with up-to-date Unicode data
- **Locale-Aware Operations**: Sorting, formatting, and text processing that respects locale rules
- **Text Segmentation**: Break text into graphemes, words, and sentences according to Unicode rules
- **Script Conversion**: Transliterate between writing systems (Greek→Latin, Cyrillic→Latin, etc.)
- **Collation**: Locale-sensitive string comparison and sorting with customizable strength levels
- **High Performance**: Built on ICU's optimized C++ implementation

## Installation

```bash
pip install uicu
```

### Dependencies

- Python 3.10+
- PyICU 2.11+
- fontTools[unicode] 4.38.0+ (for enhanced Unicode data)

## Quick Start

### Character Properties

```python
import uicu

# Get character information
char = uicu.Char('€')
print(char.name)         # 'EURO SIGN'
print(char.category)     # 'Sc' (Currency Symbol)
print(char.script)       # 'Zyyy' (Common)
print(char.block)        # 'Currency Symbols'

# Direct function access
print(uicu.name('你'))    # 'CJK UNIFIED IDEOGRAPH-4F60'
print(uicu.script('A'))   # 'Latn'

# Note: Multi-codepoint strings (like flag emojis) need special handling
# char = uicu.Char('🎉')  # ✅ Works: Party popper (single codepoint)
# char = uicu.Char('🇺🇸')  # ❌ Fails: US flag (two codepoints)
```

### Locale-Aware Collation

```python
import uicu

# Create a locale-specific collator
collator = uicu.Collator('de-DE')  # German collation rules

# Sort strings according to locale
words = ['Müller', 'Mueller', 'Mahler']
sorted_words = collator.sort(words)
print(sorted_words)  # German-specific ordering

# Numeric sorting
numeric_collator = uicu.Collator('en-US', numeric=True)
items = ['item10', 'item2', 'item1']
print(numeric_collator.sort(items))  # ['item1', 'item2', 'item10']

# Direct comparison
print(uicu.compare('café', 'cafe', 'en-US'))  # 1 (café > cafe)
```

### Text Segmentation

```python
import uicu

# Break text into user-perceived characters (grapheme clusters)
text = "👨‍👩‍👧‍👦"  # Family emoji
print(list(uicu.graphemes(text)))  # ['👨‍👩‍👧‍👦'] - single grapheme!

# Word segmentation
text = "Hello, world! How are you?"
words = list(uicu.words(text))
print(words)  # ['Hello', 'world', 'How', 'are', 'you']

# Sentence segmentation
text = "Dr. Smith went to N.Y.C. yesterday. He's busy!"
sentences = list(uicu.sentences(text))
print(sentences)  # Handles abbreviations correctly

# Language-specific segmentation
thai_text = "สวัสดีครับ"
thai_words = list(uicu.words(thai_text, locale='th-TH'))
```

### Script Conversion and Transliteration

```python
import uicu

# Convert between scripts
trans = uicu.Transliterator('Greek-Latin')
print(trans.transliterate('Ελληνικά'))  # 'Ellēniká'

# Remove accents
trans = uicu.Transliterator('Latin-ASCII')
print(trans.transliterate('café résumé'))  # 'cafe resume'

# Chain transformations
trans = uicu.Transliterator('Any-Latin; Latin-ASCII; Lower')
print(trans.transliterate('北京'))  # 'bei jing'

# Case transformations
upper = uicu.Transliterator('Upper')
print(upper.transliterate('hello'))  # 'HELLO'
```

### Working with Locales

```python
import uicu

# Create and inspect locales
locale = uicu.Locale('zh-Hant-TW')
print(locale.language)     # 'zh'
print(locale.script)       # 'Hant'
print(locale.region)       # 'TW'
print(locale.display_name) # 'Chinese (Traditional, Taiwan)'

# Get system default locale
default = uicu.get_default_locale()
print(default.language_tag)  # e.g., 'en-US'

# List available locales
locales = uicu.get_available_locales()
print(f"Available locales: {len(locales)}")  # 700+ locales

# Create locale-specific services
formatter = locale.get_datetime_formatter(date_style='long', time_style='short')
# Note: Formatting works but parsing is currently broken
```

## Advanced Usage

### Custom Collation Strength

```python
# Primary strength - ignores case and accents
collator = uicu.Collator('en-US', strength='primary')
print(collator.compare('café', 'CAFE'))  # 0 (equal)

# Secondary strength - considers accents but not case
collator = uicu.Collator('en-US', strength='secondary')
print(collator.compare('café', 'CAFÉ'))  # 0 (equal)
print(collator.compare('café', 'cafe'))  # 1 (café > cafe)

# Tertiary strength (default) - considers case
collator = uicu.Collator('en-US', strength='tertiary')
print(collator.compare('café', 'Café'))  # 1 (café > Café)
```

### Reusable Segmenters

```python
# Create reusable segmenters for better performance
word_segmenter = uicu.WordSegmenter('en-US')
sentences = [
    "This is a test.",
    "Another sentence here.",
    "And one more!"
]

for sentence in sentences:
    words = list(word_segmenter.segment(sentence))
    print(f"{len(words)} words: {words}")
```

### Script Detection

```python
# Detect the primary script in text
print(uicu.detect_script('Hello'))      # 'Latn'
print(uicu.detect_script('你好'))        # 'Hani'
print(uicu.detect_script('مرحبا'))      # 'Arab'
print(uicu.detect_script('Привет'))     # 'Cyrl'
```

## API Design Philosophy

`uicu` follows these principles:

1. **Pythonic**: Natural Python idioms, not C++ style
2. **Unicode-first**: Seamless handling of all Unicode text
3. **Locale-aware**: Respect cultural and linguistic differences
4. **Performance**: Efficient ICU algorithms under the hood
5. **Compatibility**: Works with Python's built-in string types
6. **Fallbacks**: Graceful degradation when optional features unavailable

## Development Status

### Version 0.1.1 (2025-01-25)

Currently implemented:
- ✅ Unicode character properties with fontTools.unicodedata integration
- ✅ Locale management with BCP 47 support
- ✅ Collation and sorting with customizable strength levels
- ✅ Text segmentation (graphemes, words, sentences, line breaks)
- ✅ Transliteration and script conversion
- ✅ Script detection for text analysis
- ✅ Comprehensive exception hierarchy
- ✅ Type hints throughout for better IDE support
- ⚡ Date/time formatting (partial - formatting works, parsing needs fixes)
- ✅ Comprehensive example script demonstrating all features

Recent improvements:
- 🔧 Fixed all critical linting issues for better code quality
- 🔧 Modernized type hints to use built-in types
- 🔧 Improved error handling with specific exceptions
- 🔧 Optimized imports and removed unused code
- 🆕 Added DateTimeFormatter with style-based and pattern-based formatting
- 🆕 Added date range formatting support
- 🆕 Added comprehensive demo script (`examples/uicu_demo.py`)

Coming soon:
- ⏳ Fix date/time parsing functionality
- ⏳ Number formatting (decimal, currency, percent, scientific)
- ⏳ Message formatting with plural/gender support
- ⏳ List formatting with locale-appropriate conjunctions
- ⏳ Relative time formatting ("3 days ago", "in 2 hours")
- ⏳ Calendar operations
- ⏳ Advanced timezone handling
- ⏳ Unicode regex support
- ⏳ Bidirectional text layout
- ⏳ Unicode security (confusables, spoofing detection)
- ⏳ Number spellout
- ⏳ Performance benchmarks
- ⏳ Sphinx documentation

## Examples

Run the comprehensive demo to see all features in action:

```bash
python examples/uicu_demo.py
```

This demo includes:
1. Unicode character exploration with properties
2. Culture-aware multilingual name sorting
3. Text segmentation (graphemes, words, sentences)
4. Script conversion and transliteration
5. Locale-aware date/time formatting
6. Smart numeric vs lexical sorting
7. Unicode text transformations
8. Automatic script detection
9. Thai word segmentation
10. Emoji and complex grapheme handling
11. Case-sensitive sorting control
12. Bidirectional text analysis

## Development

### Environment Setup

```bash
# Install and use uv for package management
pip install uv

# Use hatch for development workflow
uv pip install hatch
```

### Common Development Tasks

```bash
# Activate development environment
hatch shell

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format

# Run type checking
hatch run type-check
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [PyICU](https://pypi.org/project/PyICU/), which provides Python bindings for ICU
- Enhanced with [fontTools.unicodedata](https://github.com/fonttools/fonttools) for up-to-date Unicode data
- Inspired by the need for more Pythonic Unicode handling in Python applications