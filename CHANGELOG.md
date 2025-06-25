# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-01-25

### Added

- Initial implementation of `uicu` package as a Pythonic wrapper around PyICU
- **Character Module (`uicu.char`)**: Unicode character properties with fontTools.unicodedata integration
  - Basic properties: name, category, bidirectional, combining, mirrored
  - Numeric properties: decimal, digit, numeric
  - Script properties: script, script_name, script_extensions, script_direction
  - Block property for Unicode block identification
  - Rich `Char` class for object-oriented access to character properties
  - Automatic fallback to built-in unicodedata when fontTools is unavailable
  
- **Locale Module (`uicu.locale`)**: Central locale management and factory
  - BCP 47 locale identifier support (both hyphen and underscore separators)
  - Factory methods for creating locale-aware services
  - Properties: language, script, region, variant, display_name
  - Convenience functions: get_available_locales(), get_default_locale()
  
- **Collation Module (`uicu.collate`)**: Locale-aware string comparison and sorting
  - Configurable comparison strength levels (primary through identical)
  - Numeric sorting support (2 < 10)
  - Case ordering options (upper first/lower first)
  - Sort key generation for efficient sorting
  - Callable interface for use with sorted()
  - Convenience functions: sort(), compare()
  
- **Segmentation Module (`uicu.segment`)**: Text boundary analysis
  - Grapheme cluster segmentation (user-perceived characters)
  - Word segmentation with locale-specific rules
  - Sentence segmentation with abbreviation handling
  - Line break opportunity detection
  - Reusable segmenter classes for better performance
  - UTF-16 to Python string index conversion
  
- **Transliteration Module (`uicu.translit`)**: Script conversion and text transforms
  - Script-to-script conversion (e.g., Greek→Latin, Cyrillic→Latin)
  - Unicode normalization (NFC, NFD, NFKC, NFKD)
  - Case transformations (upper, lower, title)
  - Compound transform support
  - Custom rule-based transliterators
  - Inverse transform support
  - Filter function for selective transliteration
  
- **Exception Hierarchy**: Clear, specific exception types
  - UICUError: Base exception for all uicu errors
  - ConfigurationError: Invalid configuration
  - CollationError: Collation-specific errors
  - SegmentationError: Segmentation-specific errors
  - TransliterationError: Transliteration-specific errors
  
- **Testing Infrastructure**: Comprehensive test suite
  - 62 tests covering all implemented functionality
  - Tests for edge cases and error conditions
  - Locale-specific behavior tests
  
### Technical Details

- Uses PyICU 2.11+ for core Unicode functionality
- Integrates fontTools.unicodedata for up-to-date Unicode data
- Supports Python 3.10+
- Follows PEP 8 coding standards
- Type hints throughout for better IDE support
- Detailed docstrings with examples

### Known Limitations

- Formatting module (dates, numbers, messages) not yet implemented
- Documentation and usage examples pending
- Some ICU features not yet exposed through Pythonic interface