# API Reference

This section provides detailed API documentation for all UICU modules and classes.

## Core Modules

### Character Properties
**[`uicu.char`](char.md)** - Unicode character analysis and properties
- [`Char`](char.md#uicu.char.Char) - Character property class
- [`name()`](char.md#uicu.char.name) - Get character name
- [`category()`](char.md#uicu.char.category) - Get character category
- [`script()`](char.md#uicu.char.script) - Get character script
- [`block()`](char.md#uicu.char.block) - Get character block

### Locale Management
**[`uicu.locale`](locale.md)** - Locale handling and services
- [`Locale`](locale.md#uicu.locale.Locale) - Locale representation
- [`get_default_locale()`](locale.md#uicu.locale.get_default_locale) - System default locale
- [`get_available_locales()`](locale.md#uicu.locale.get_available_locales) - List available locales

### Text Collation
**[`uicu.collate`](collate.md)** - Locale-aware text sorting and comparison
- [`Collator`](collate.md#uicu.collate.Collator) - Text collation class
- [`compare()`](collate.md#uicu.collate.compare) - Compare two strings
- [`sort()`](collate.md#uicu.collate.sort) - Sort a list of strings

### Text Segmentation
**[`uicu.segment`](segment.md)** - Text boundary analysis and segmentation
- [`GraphemeSegmenter`](segment.md#uicu.segment.GraphemeSegmenter) - Grapheme cluster segmentation
- [`WordSegmenter`](segment.md#uicu.segment.WordSegmenter) - Word boundary detection
- [`SentenceSegmenter`](segment.md#uicu.segment.SentenceSegmenter) - Sentence boundary detection
- [`LineSegmenter`](segment.md#uicu.segment.LineSegmenter) - Line break detection

### Transliteration
**[`uicu.translit`](translit.md)** - Script conversion and text transformation
- [`Transliterator`](translit.md#uicu.translit.Transliterator) - Text transformation class
- [`transliterate()`](translit.md#uicu.translit.transliterate) - Transform text
- [`get_available_transforms()`](translit.md#uicu.translit.get_available_transforms) - List transforms

### Date/Time Formatting
**[`uicu.format`](format.md)** - Locale-aware date and time formatting
- [`DateTimeFormatter`](format.md#uicu.format.DateTimeFormatter) - Date/time formatting class

### Exceptions
**[`uicu.exceptions`](exceptions.md)** - Exception classes
- [`UICUError`](exceptions.md#uicu.exceptions.UICUError) - Base exception class
- [`ConfigurationError`](exceptions.md#uicu.exceptions.ConfigurationError) - Configuration errors
- [`OperationError`](exceptions.md#uicu.exceptions.OperationError) - Operation errors

### Utilities
**[`uicu._utils`](utils.md)** - Internal utilities and helpers

## Quick Reference

### Most Common Functions

```python
import uicu

# Character properties
char = uicu.Char('€')
name = uicu.name('€')
category = uicu.category('€')
script = uicu.script('€')

# Locale operations
locale = uicu.Locale('en-US')
default = uicu.get_default_locale()
available = uicu.get_available_locales()

# Text collation
result = uicu.compare('café', 'cafe', 'en-US')
sorted_list = uicu.sort(['banana', 'apple'], 'en-US')

# Text segmentation
graphemes = list(uicu.graphemes('Hello 👨‍👩‍👧‍👦'))
words = list(uicu.words('Hello, world!'))
sentences = list(uicu.sentences('Hello. How are you?'))

# Transliteration
result = uicu.transliterate('Ελληνικά', 'Greek-Latin')

# Script detection
script = uicu.detect_script('Hello 世界')
```

### Class-Based API

```python
# Create reusable objects for better performance
collator = uicu.Collator('de-DE', numeric=True)
segmenter = uicu.WordSegmenter('th-TH')
trans = uicu.Transliterator('Latin-ASCII')

# Use them multiple times
sorted1 = collator.sort(list1)
sorted2 = collator.sort(list2)

words1 = list(segmenter.segment(text1))
words2 = list(segmenter.segment(text2))
```

## Module Organization

```
uicu/
├── __init__.py       # Package initialization and exports
├── char.py          # Character properties and analysis
├── locale.py        # Locale management and factories
├── collate.py       # Text collation and sorting
├── segment.py       # Text segmentation and boundaries
├── translit.py      # Transliteration and transformation
├── format.py        # Date/time formatting
├── exceptions.py    # Exception classes
└── _utils.py        # Internal utilities
```

## Type Annotations

All UICU functions and methods include type annotations:

```python
def compare(
    text1: str,
    text2: str,
    locale: str | Locale = 'en-US',
    strength: str = 'tertiary'
) -> int:
    """Compare two strings according to locale rules."""
```

## Import Patterns

### Basic Import
```python
import uicu

# Use fully qualified names
char = uicu.Char('A')
locale = uicu.Locale('en-US')
```

### Specific Imports
```python
from uicu import Char, Locale, Collator

# Use directly
char = Char('A')
locale = Locale('en-US')
collator = Collator('en-US')
```

### Function Imports
```python
from uicu import compare, sort, graphemes, words

# Use convenience functions
result = compare('a', 'b')
sorted_list = sort(['c', 'a', 'b'])
```

## Performance Notes

1. **Object Creation**: Creating ICU objects (Collator, Transliterator, etc.) is expensive. Reuse them when possible.

2. **Locale Objects**: Cache and reuse Locale objects for better performance.

3. **Batch Operations**: Process multiple items with the same configuration together.

4. **Memory Usage**: ICU objects can use significant memory. Use object pools for large applications.

## Version Information

```python
import uicu
print(uicu.__version__)  # Current UICU version

import icu
print(icu.ICU_VERSION)  # Underlying ICU version
```

## Error Handling

All UICU operations may raise exceptions:

```python
try:
    char = uicu.Char('invalid string')
except uicu.UICUError as e:
    print(f"Error: {e}")

try:
    locale = uicu.Locale('invalid-locale')
except uicu.ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Thread Safety

ICU objects are generally thread-safe for read operations:
- ✅ Safe: Multiple threads using the same Collator to sort
- ❌ Unsafe: Multiple threads modifying the same object
- ✅ Recommended: Create separate objects per thread or use thread-local storage

## Next Steps

- Browse individual module documentation for detailed API information
- See the [User Guide](../guide/index.md) for usage examples
- Check [Examples](../examples/index.md) for real-world use cases