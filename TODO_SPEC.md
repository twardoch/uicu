# uicu Package Specification

## Executive Summary

The `uicu` package provides a Pythonic, natural, and performant wrapper around PyICU, supplemented by fontTools.unicodedata. It exposes ICU's powerful internationalization capabilities through intuitive Python interfaces, making advanced Unicode operations accessible to Python developers without requiring knowledge of ICU's C++ heritage.

## Package Objectives

1. **Pythonic API**: Transform PyICU's C++-style interface into idiomatic Python
2. **Rich Objects**: Provide well-documented classes that encapsulate Unicode functionality
3. **Native Integration**: Work seamlessly with Python's built-in types (str, datetime, etc.)
4. **Performance**: Maintain ICU's performance with minimal wrapper overhead
5. **Comprehensive Coverage**: Expose all major ICU functionality through intuitive interfaces

## Architecture

### Module Structure

```
src/uicu/
├── __init__.py       # Package initialization, convenience imports
├── __version__.py    # Version info (managed by hatch-vcs)
├── char.py          # Unicode character properties
├── locale.py        # Locale class and locale-aware factories
├── collate.py       # Collation and locale-aware sorting
├── format.py        # Date, number, list, and message formatting
├── segment.py       # Text segmentation (graphemes, words, sentences)
├── translit.py      # Transliteration and text transforms
├── exceptions.py    # Custom exception hierarchy
└── _utils.py        # Internal utilities (not public API)
```

### Design Principles

1. **Immutability**: Prefer immutable operations, return new objects rather than modifying in-place
2. **Type Safety**: Use type hints throughout, accept and return native Python types
3. **Error Clarity**: Wrap ICU errors in meaningful Python exceptions
4. **Thread Safety**: Document thread safety, avoid global mutable state
5. **Lazy Loading**: Import heavy dependencies only when needed

## Module Specifications

### 1. Character Properties Module (uicu.char)

**Purpose**: Provide Unicode character information using the latest Unicode data.

**Implementation Strategy**:
- Primary source: fontTools.unicodedata for up-to-date Unicode data
- Fallback: Python's built-in unicodedata if fontTools unavailable
- Accept both single characters and integer codepoints

**Core Functions**:
```python
# Basic properties (delegate to fontTools.unicodedata)
def name(char: Union[str, int], default: str = None) -> str:
    """Return Unicode name of character."""

def category(char: Union[str, int]) -> str:
    """Return general category (e.g., 'Lu' for uppercase letter)."""

def bidirectional(char: Union[str, int]) -> str:
    """Return bidirectional class."""

def combining(char: Union[str, int]) -> int:
    """Return canonical combining class."""

def mirrored(char: Union[str, int]) -> bool:
    """Return True if character is mirrored in bidi text."""

def decimal(char: Union[str, int], default: Any = None) -> int:
    """Return decimal value of character."""

def digit(char: Union[str, int], default: Any = None) -> int:
    """Return digit value of character."""

def numeric(char: Union[str, int], default: Any = None) -> Union[int, float]:
    """Return numeric value of character."""

# Script and block properties (unique to fontTools)
def script(char: Union[str, int]) -> str:
    """Return ISO 15924 script code (e.g., 'Latn', 'Hani')."""

def script_name(code: str) -> str:
    """Return human-readable script name."""

def script_extensions(char: Union[str, int]) -> Set[str]:
    """Return set of scripts that use this character."""

def block(char: Union[str, int]) -> str:
    """Return Unicode block name."""

def script_direction(script_code: str) -> str:
    """Return 'LTR' or 'RTL' for script direction."""
```

**Optional OOP Interface**:
```python
class Char:
    """Rich Unicode character object."""
    def __init__(self, char: Union[str, int]):
        self._char = char if isinstance(char, str) else chr(char)
        
    @property
    def name(self) -> str: ...
    @property
    def category(self) -> str: ...
    @property
    def script(self) -> str: ...
    # ... other properties
    
    def __str__(self) -> str:
        return self._char
    
    def __repr__(self) -> str:
        return f"<Char {self._char!r} U+{ord(self._char):04X}>"
```

### 2. Locale Module (uicu.locale)

**Purpose**: Central locale management and factory for locale-aware services.

**Implementation**:
```python
class Locale:
    """Represents a specific locale and creates locale-aware services."""
    
    def __init__(self, identifier: str):
        """Create locale from BCP 47 identifier (e.g., 'en-GB', 'zh-Hant-TW')."""
        self._icu_locale = icu.Locale.createCanonical(identifier)
        if not self._icu_locale.getLanguage():
            raise ConfigurationError(f"Invalid locale identifier: {identifier}")
    
    # Properties
    @property
    def display_name(self) -> str:
        """Full human-readable name in default locale."""
    
    @property
    def language(self) -> str:
        """ISO 639 language code."""
    
    @property
    def script(self) -> str:
        """ISO 15924 script code if specified."""
    
    @property
    def region(self) -> str:
        """ISO 3166 region code."""
    
    # Factory methods
    def get_collator(self, strength: str = 'tertiary', 
                     numeric: bool = False) -> 'Collator':
        """Create a collator for this locale."""
    
    def get_datetime_formatter(self, date_style: str = 'medium',
                              time_style: str = 'medium') -> 'DateTimeFormatter':
        """Create a date/time formatter."""
    
    def get_number_formatter(self, style: str = 'decimal') -> 'NumberFormatter':
        """Create a number formatter."""
    
    def get_list_formatter(self, style: str = 'standard',
                          list_type: str = 'and') -> 'ListFormatter':
        """Create a list formatter."""
    
    def get_word_segmenter(self) -> 'WordSegmenter':
        """Create a word segmenter for this locale."""
```

### 3. Collation Module (uicu.collate)

**Purpose**: Locale-aware string comparison and sorting.

**Implementation**:
```python
class Collator:
    """Locale-aware string collator for sorting."""
    
    def __init__(self, locale: Union[str, Locale], 
                 strength: str = 'tertiary',
                 numeric: bool = False):
        """
        Create a collator.
        
        Args:
            locale: Locale identifier or Locale object
            strength: 'primary' (base letters only), 'secondary' (+accents),
                     'tertiary' (+case), 'quaternary' (+variants), 'identical'
            numeric: Enable numeric sorting (2 < 10)
        """
    
    def compare(self, a: str, b: str) -> int:
        """Compare strings: -1 if a<b, 0 if a==b, 1 if a>b."""
    
    def key(self, s: str) -> bytes:
        """Return sort key for string (for use with sorted())."""
    
    def __call__(self, s: str) -> bytes:
        """Alias for key() to use as sorted() key function."""
    
    def sort(self, strings: Iterable[str]) -> List[str]:
        """Return sorted copy of strings."""

# Convenience functions
def sort(strings: Iterable[str], locale: Union[str, Locale], **options) -> List[str]:
    """Sort strings according to locale rules."""
    return Collator(locale, **options).sort(strings)
```

### 4. Format Module (uicu.format)

**Purpose**: Locale-aware formatting for dates, numbers, and messages.

**Implementation**:
```python
class DateTimeFormatter:
    """Formats datetime objects according to locale conventions."""
    
    def __init__(self, locale: Union[str, Locale],
                 date_style: str = 'medium',
                 time_style: str = 'medium',
                 pattern: str = None,
                 timezone: Union[str, tzinfo] = None):
        """
        Create formatter.
        
        Args:
            date_style/time_style: 'full', 'long', 'medium', 'short', 'none'
            pattern: Custom pattern like 'yyyy-MM-dd'
            timezone: Timezone for formatting
        """
    
    def format(self, dt: datetime) -> str:
        """Format datetime to string."""
    
    def parse(self, text: str) -> datetime:
        """Parse string to datetime."""

class NumberFormatter:
    """Formats numbers according to locale conventions."""
    
    def __init__(self, locale: Union[str, Locale],
                 style: str = 'decimal',
                 min_fraction_digits: int = None,
                 max_fraction_digits: int = None):
        """
        Create formatter.
        
        Args:
            style: 'decimal', 'percent', 'currency', 'scientific'
        """
    
    def format(self, number: Union[int, float]) -> str:
        """Format number to string."""
    
    def format_currency(self, amount: Union[int, float], 
                       currency: str) -> str:
        """Format as currency (e.g., currency='USD')."""

class ListFormatter:
    """Joins lists with locale-appropriate conjunctions."""
    
    def __init__(self, locale: Union[str, Locale],
                 style: str = 'standard',
                 list_type: str = 'and'):
        """
        Create formatter.
        
        Args:
            style: 'standard', 'narrow', etc.
            list_type: 'and', 'or', 'units'
        """
    
    def format(self, items: Iterable[str]) -> str:
        """Join items with appropriate separators and conjunctions."""

class MessageFormatter:
    """ICU message format with plural/gender support."""
    
    def __init__(self, locale: Union[str, Locale], pattern: str):
        """Create formatter with ICU message pattern."""
    
    def format(self, **kwargs) -> str:
        """Format message with parameters."""
```

### 5. Segmentation Module (uicu.segment)

**Purpose**: Text boundary analysis (graphemes, words, sentences).

**Key Implementation Detail**: Must handle UTF-16 index conversion since ICU uses UTF-16 internally.

**Implementation**:
```python
def graphemes(text: str, locale: Union[str, Locale] = None) -> Iterator[str]:
    """
    Iterate over grapheme clusters (user-perceived characters).
    
    Example:
        list(graphemes('🇨🇦')) -> ['🇨🇦']  # Single flag emoji
        list(graphemes('e\u0301')) -> ['é']  # Combined character
    """

def words(text: str, locale: Union[str, Locale] = None,
          skip_whitespace: bool = False) -> Iterator[str]:
    """
    Iterate over words according to locale rules.
    
    Note: Includes punctuation and whitespace as separate tokens
    unless skip_whitespace=True.
    """

def sentences(text: str, locale: Union[str, Locale] = None) -> Iterator[str]:
    """Iterate over sentences according to locale rules."""

# Optional OOP interface
class GraphemeSegmenter:
    """Reusable grapheme segmenter."""
    def __init__(self, locale: Union[str, Locale] = None):
        self._break_iterator = self._create_break_iterator(locale)
    
    def segment(self, text: str) -> Iterator[str]:
        """Segment text into graphemes."""

class WordSegmenter:
    """Reusable word segmenter."""
    # Similar implementation

class SentenceSegmenter:
    """Reusable sentence segmenter."""
    # Similar implementation
```

### 6. Transliteration Module (uicu.translit)

**Purpose**: Script conversion and text transforms.

**Implementation**:
```python
def transliterate(text: str, transform_id: str, 
                  direction: str = 'forward') -> str:
    """
    Apply transliteration transform.
    
    Args:
        text: Input text
        transform_id: ICU transform ID (e.g., 'Greek-Latin', 'Any-NFD')
        direction: 'forward' or 'reverse'
    
    Example:
        transliterate('Ελληνικά', 'Greek-Latin') -> 'Ellēniká'
    """

def get_available_transforms() -> List[str]:
    """Return list of available transform IDs."""

class Transliterator:
    """Reusable transliterator for better performance."""
    
    def __init__(self, transform_id: str, direction: str = 'forward'):
        """Create transliterator."""
    
    def transliterate(self, text: str) -> str:
        """Apply transliteration."""
    
    def inverse(self) -> 'Transliterator':
        """Return inverse transliterator."""
    
    @classmethod
    def from_rules(cls, name: str, rules: str, 
                   direction: str = 'forward') -> 'Transliterator':
        """Create from custom rules."""
```

### 7. Exception Hierarchy (uicu.exceptions)

**Purpose**: Clear, specific error handling.

```python
class UICUError(Exception):
    """Base exception for all uicu errors."""

class ConfigurationError(UICUError):
    """Invalid configuration (locale, pattern, etc.)."""

class FormattingError(UICUError):
    """Error during formatting operations."""

class CollationError(UICUError):
    """Error in collation operations."""

class SegmentationError(UICUError):
    """Error in text segmentation."""

class TransliterationError(UICUError):
    """Error in transliteration."""
```

## Implementation Guidelines

### Type Conversion

1. **Input**: Accept Python native types (str, datetime, int, float)
2. **Internal**: Convert to ICU types (UnicodeString, UDate) as needed
3. **Output**: Always return Python native types

### Error Handling

```python
try:
    icu_result = icu_function(...)
except icu.ICUError as e:
    raise AppropriateUICUError(f"Meaningful message: {e}") from e
```

### Performance Considerations

1. **Object Reuse**: Encourage reusing Collator, Formatter, Segmenter objects
2. **Caching**: Cache expensive objects internally where safe
3. **Lazy Imports**: Import ICU modules only when needed
4. **String Conversion**: Minimize conversions between Python str and ICU UnicodeString

### Thread Safety

- Document which objects are thread-safe (most ICU objects are not)
- Avoid module-level mutable state
- Consider thread-local storage for caches if needed

## Testing Requirements

### Unit Tests (pytest)

1. **Character Properties**: Test various scripts, blocks, categories
2. **Locale**: Test valid/invalid identifiers, factory methods
3. **Collation**: Test sorting in different locales, strength levels
4. **Formatting**: Test date/number formatting with various locales
5. **Segmentation**: Test with emoji, combining characters, various scripts
6. **Transliteration**: Test common transforms, bidirectional conversion

### Edge Cases

- Empty strings
- Invalid input (wrong types, invalid locales)
- Non-BMP characters (emoji, rare scripts)
- RTL text and mixed-direction text
- Very long strings (performance)

### Integration Tests

- Cross-module functionality (e.g., Locale creating formatters)
- Real-world text processing scenarios
- Performance comparison with raw PyICU

## Documentation Requirements

### API Documentation

- Comprehensive docstrings for all public APIs
- Type hints throughout
- Examples in docstrings
- Link to relevant Unicode/ICU documentation

### User Guide

1. **Getting Started**: Installation, basic usage
2. **Character Information**: Using char module
3. **Internationalization**: Locale, formatting, collation
4. **Text Processing**: Segmentation, transliteration
5. **Best Practices**: Performance tips, common patterns

### Examples

Create an `examples/` directory with:
- basic_usage.py
- multilingual_sorting.py
- text_segmentation.py
- formatting_examples.py
- transliteration_demo.py

## Development Workflow

1. **Setup Environment**: Install PyICU and fonttools[unicode]
2. **Implement Core**: Start with char.py and locale.py
3. **Add Features**: Implement each module with tests
4. **Documentation**: Write docs alongside code
5. **Performance**: Profile and optimize critical paths
6. **Polish**: Add examples, improve error messages

## Success Metrics

1. **Completeness**: All specified APIs implemented
2. **Testing**: >95% test coverage
3. **Performance**: <10% overhead vs raw PyICU
4. **Documentation**: All public APIs documented with examples
5. **Usability**: Clean, intuitive API that "feels right" to Python developers

## Future Enhancements

- Unicode regex support
- Bidirectional text layout
- Calendar systems
- Unicode security (confusables, spoofing)
- Number spellout
- Time zone handling
- Message extraction for i18n