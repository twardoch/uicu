# Specification for `uicu` Package

## 1. Introduction
The `uicu` package is a Pythonic wrapper around [PyICU](https://pypi.org/project/pyicu/), which provides Python bindings for the [ICU library](https://unicode-org.github.io/icu/). The goal is to create an intuitive, well-documented, and performant API that integrates seamlessly with Python’s native Unicode handling (`str`) while exposing ICU’s rich functionality, including Unicode properties, locale handling, formatting, collation, transliteration, and text segmentation. The package may incorporate [fontTools.unicodedata](https://fonttools.readthedocs.io/en/latest/unicodedata/index.html) for specific Unicode data needs, such as writing system information, if it provides advantages over ICU.

This specification outlines the package structure, API design, and implementation guidelines to assist a junior developer in building `uicu`. It includes detailed examples, performance considerations, and documentation standards.

## 2. Package Structure
The `uicu` package will be organized into submodules to reflect ICU’s major components, ensuring modularity and ease of use. The proposed structure is:

- `uicu/__init__.py`: Top-level imports, package metadata, and high-level convenience functions.
- `uicu/unicode.py`: Functions for Unicode character properties and string operations.
- `uicu/locale.py`: Classes and functions for locale handling.
- `uicu/format.py`: Classes for formatting and parsing dates, numbers, and messages.
- `uicu/collation.py`: Functions and classes for locale-aware string comparison and sorting.
- `uicu/transliterate.py`: Functions for transliteration.
- `uicu/breakiter.py`: Classes for text segmentation (e.g., word or sentence boundaries).

Each module will provide Pythonic interfaces, either as functions operating on native Python types (e.g., `str`) or as classes wrapping PyICU objects with simplified methods.

## 3. API Design Principles
To ensure the API is Pythonic, natural, and performant, the following principles will guide development:

- **Simplicity**: Provide high-level functions for common tasks (e.g., `uicu.format_date()` instead of multiple PyICU steps).
- **Integration with Python**: Use Python’s `str` for string operations where possible, supplementing with ICU for advanced functionality.
- **Consistency**: Follow PEP 8 naming conventions (e.g., `lowercase_with_underscores` for functions) and use exceptions for error handling.
- **Performance**: Minimize wrapper overhead by directly calling PyICU methods where feasible.
- **Documentation**: Include detailed docstrings with examples, type hints, and references to ICU documentation.
- **Flexibility**: Offer both simple functions for quick tasks and classes for advanced use cases requiring fine-grained control.

## 4. Detailed API Specification

### 4.1. `uicu.unicode`
This module handles Unicode character properties and string operations, leveraging ICU’s `uchar` module and `UnicodeString` class.

#### Functions
- `normalize(text: str, form: str = 'NFC') -> str`
  - Normalizes a string using ICU’s Normalizer2.
  - Parameters:
    - `text`: Input string to normalize.
    - `form`: Normalization form (`'NFC'`, `'NFD'`, `'NFKC'`, `'NFKD'`).
  - Returns: Normalized Python `str`.
  - Example:
    ```python
    import uicu
    text = "café"
    normalized = uicu.normalize(text, 'NFD')  # Decomposes 'é' into 'e' + combining acute accent
    ```
- `get_category(char: str) -> str`
  - Returns the Unicode general category of a single character (e.g., `'Lu'` for uppercase letter).
  - Uses ICU’s `u_charType` or fontTools.unicodedata’s `category` if specified.
  - Example:
    ```python
    category = uicu.get_category('A')  # Returns 'Lu'
    ```
- `is_alpha(char: str) -> bool`
  - Checks if a character is alphabetic using ICU’s `u_isalpha`.
  - Example:
    ```python
    is_alpha = uicu.is_alpha('α')  # Returns True
    ```

#### Classes
- `UnicodeString`
  - Wraps `icu.UnicodeString` for advanced string operations.
  - Methods:
    - `__str__()`: Converts to Python `str`.
    - `normalize(form: str = 'NFC') -> str`: Normalizes the string.
    - `to_upper(locale: str = None) -> str`: Converts to uppercase, optionally locale-aware.
  - Example:
    ```python
    from uicu import UnicodeString
    us = UnicodeString("café")
    upper = us.to_upper(locale='tr_TR')  # Turkish uppercase rules
    ```

### 4.2. `uicu.locale`
This module provides locale handling, wrapping `icu.Locale`.

#### Classes
- `Locale`
  - Wraps `icu.Locale` with Pythonic properties.
  - Properties:
    - `language`: Returns the language code (e.g., `'en'`).
    - `display_name`: Returns the locale’s display name.
  - Methods:
    - `get_available() -> List[str]`: Returns available locale IDs.
  - Example:
    ```python
    from uicu import Locale
    loc = Locale('fr_FR')
    print(loc.display_name)  # Prints "French (France)"
    ```

#### Context Manager
- `set_locale(locale: str)`
  - Temporarily sets the default locale for ICU operations.
  - Example:
    ```python
    with uicu.set_locale('es_ES'):
        formatted = uicu.format_number(1234.56)  # Uses Spanish formatting
    ```

### 4.3. `uicu.format`
This module handles formatting and parsing for dates, numbers, and messages.

#### Classes
- `DateFormatter`
  - Wraps `icu.DateFormat` for date and time formatting.
  - Methods:
    - `format(dt: datetime) -> str`: Formats a datetime object.
    - `parse(text: str) -> datetime`: Parses a string to a datetime.
  - Example:
    ```python
    from uicu import DateFormatter
    formatter = DateFormatter(locale='en_US', pattern='MMM d, y')
    formatted = formatter.format(datetime.now())  # e.g., "Oct 25, 2025"
    ```
- `NumberFormatter`
  - Wraps `icu.NumberFormat` for number formatting.
  - Methods:
    - `format(number: float) -> str`: Formats a number.
  - Example:
    ```python
    formatter = uicu.NumberFormatter(locale='de_DE')
    formatted = formatter.format(1234.56)  # e.g., "1.234,56"
    ```

#### Functions
- `format_date(dt: datetime, locale: str = None, pattern: str = None) -> str`
  - Convenience function for date formatting.
  - Example:
    ```python
    formatted = uicu.format_date(datetime.now(), locale='en_US', pattern='MMM d, y')
    ```

### 4 U.4. `uicu.collation`
This module provides locale-aware string comparison and sorting.

#### Functions
- `sorted(strings: List[str], locale: str = None) -> List[str]`
  - Sorts strings using ICU’s collation rules.
  - Example:
    ```python
    strings = ['café', 'cafe']
    sorted_list = uicu.sorted(strings, locale='fr_FR')  # Locale-aware sorting
    ```

#### Classes
- `Collator`
  - Wraps `icu.Collator` for custom collation.
  - Methods:
    - `compare(a: str, b: str) -> int`: Compares two strings.
  - Example:
    ```python
    from uicu import Collator
    collator = Collator(locale='fr_FR')
    sorted_list = sorted(strings, key=collator)
    ```

### 4.5. `uicu.transliterate`
This module handles transliteration.

#### Functions
- `transliterate(text: str, transform: str) -> str`
  - Transliterates text using ICU’s transliteration rules.
  - Example:
    ```python
    text = uicu.transliterate("привет", "Cyrillic-Latin")  # Returns "privet"
    ```

### 4.6. `uicu.breakiter`
This module provides text segmentation.

#### Classes
- `BreakIterator`
  - Wraps `icu.BreakIterator` for word, sentence, or line breaking.
  - Methods:
    - `boundaries(text: str) -> List[int]`: Returns boundary indices.
  - Example:
    ```python
    from uicu import BreakIterator
    bi = BreakIterator('word', locale='en_US')
    boundaries = bi.boundaries("Hello world!")  # Returns word boundary indices
    ```

## 5. Integration with fontTools.unicodedata
The `uicu.unicode` module will include an optional parameter to use fontTools.unicodedata for character properties if specified (e.g., `use_fonttools=True`). This allows flexibility for users who prefer fontTools’ data, particularly for writing system information like `script` or `block`. For example:
```python
category = uicu.get_category('A', use_fonttools=True)  # Uses fontTools.unicodedata
```

## 6. Performance Considerations
- **Minimize Overhead**: Wrapper functions should call PyICU methods directly, avoiding multiple layers of abstraction.
- **Caching**: Cache frequently used objects (e.g., `Normalizer2` instances) to reduce initialization costs.
- **Native Types**: Use Python `str` for inputs and outputs where possible to avoid conversion overhead.
- **Profiling**: Test performance against PyICU to ensure minimal slowdown, using tools like `cProfile`.

## 7. Documentation Standards
- **Docstrings**: Follow Google Python Style Guide for docstrings, including Args, Returns, and Examples.
- **Type Hints**: Use type hints for all functions and methods (e.g., `str`, `List[str]`).
- **Examples**: Include practical examples in docstrings and a separate `examples/` directory.
- **Tutorials**: Provide tutorials in the documentation, built with [Sphinx](https://www.sphinx-doc.org/).
- **References**: Link to ICU documentation for advanced details.

## 8. Implementation Guidelines
- **Dependencies**: Require `PyICU>=2.8` and optionally `fonttools[unicodedata]>=4.38.0`.
- **Testing**: Use `pytest` with unit tests covering all functions and edge cases.
- **Error Handling**: Convert ICU error codes to Python exceptions with descriptive messages.
- **Packaging**: Use `setuptools` for distribution, with clear metadata in `setup.py`.
- **Versioning**: Follow Semantic Versioning (e.g., `0.1.0` for initial release).

## 9. Example Usage
```python
import uicu
from datetime import datetime

# Normalize a string
text = "café"
normalized = uicu.normalize(text, 'NFD')

# Format a date
formatted_date = uicu.format_date(datetime.now(), locale='fr_FR', pattern='d MMM y')

# Sort strings with locale-aware collation
strings = ['café', 'cafe']
sorted_strings = uicu.sorted(strings, locale='fr_FR')

# Transliterate text
transliterated = uicu.transliterate("привет", "Cyrillic-Latin")

# Get character properties
category = uicu.get_category('A')  # Returns 'Lu'
```

## 10. Next Steps
1. **Prototype**: Implement core modules (`unicode`, `locale`, `format`) with basic functionality.
2. **Testing**: Write unit tests to verify correctness against PyICU.
3. **Documentation**: Generate initial Sphinx documentation with examples.
4. **Performance Testing**: Profile key functions to ensure minimal overhead.
5. **Community Feedback**: Release a beta version on [PyPI](https://pypi.org/) and gather feedback.

This specification provides a clear roadmap for developing `uicu`, balancing Pythonic design, performance, and comprehensive functionality.