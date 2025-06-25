# uicu Implementation Plan

## Project Overview

The `uicu` package will be a Pythonic wrapper around PyICU, supplemented by fontTools.unicodedata. It will provide a natural, performant API that exposes rich, well-documented objects integrating with Python's native Unicode handling while adding extensive Unicode functionality.

## Key Design Principles

1. **Pythonic Interface**: Hide PyICU's C++-style API behind natural Python idioms
2. **Native Type Integration**: Work seamlessly with Python's `str` type
3. **Rich Objects**: Provide well-documented classes that encapsulate Unicode functionality
4. **Performance**: Maintain PyICU's performance while adding minimal overhead
5. **Comprehensive**: Cover all major ICU functionality with intuitive APIs

## Architecture Overview

```
uicu/
├── __init__.py      # Package initialization and convenience imports
├── __version__.py   # Version management
├── char.py         # Unicode character properties
├── locale.py       # Locale handling and factory for locale-aware services
├── collate.py      # Collation and sorting
├── format.py       # Date, number, and message formatting
├── segment.py      # Text segmentation (graphemes, words, sentences)
├── translit.py     # Transliteration
├── exceptions.py   # Custom exception hierarchy
└── _utils.py       # Internal utilities
```

## Implementation Phases

### Phase 1: Foundation (Core Infrastructure)
- [ ] Set up project structure with pyproject.toml
- [ ] Configure dependencies (PyICU, fonttools[unicode])
- [ ] Create exception hierarchy
- [ ] Implement basic utilities for PyICU/Python type conversion

### Phase 2: Character Properties (uicu.char)
- [ ] Implement basic character property functions using fontTools.unicodedata
- [ ] Add script and block identification functions
- [ ] Create optional Char class for OOP interface
- [ ] Handle both string and integer (codepoint) inputs

### Phase 3: Locale System (uicu.locale)
- [ ] Create Locale class wrapping icu.Locale
- [ ] Implement locale validation and canonicalization
- [ ] Add factory methods for creating locale-aware services
- [ ] Provide convenient properties for locale components

### Phase 4: Text Segmentation (uicu.segment)
- [ ] Implement grapheme cluster iteration
- [ ] Add word segmentation with locale support
- [ ] Add sentence segmentation
- [ ] Handle UTF-16 index conversion issues

### Phase 5: Collation (uicu.collate)
- [ ] Create Collator class with Pythonic interface
- [ ] Support for strength levels and options
- [ ] Implement callable interface for use with sorted()
- [ ] Add convenience functions for one-off sorting

### Phase 6: Formatting (uicu.format)
- [ ] DateTimeFormatter with locale-aware formatting
- [ ] NumberFormatter for decimal, currency, percent
- [ ] ListFormatter for locale-correct list joining
- [ ] MessageFormatter for ICU message format

### Phase 7: Transliteration (uicu.translit)
- [ ] Simple transliterate() function
- [ ] Transliterator class for repeated use
- [ ] Support for custom rules
- [ ] Bidirectional transliteration

### Phase 8: Testing & Documentation
- [ ] Comprehensive test suite with pytest
- [ ] API documentation with Sphinx
- [ ] Usage examples and tutorials
- [ ] Performance benchmarks

## Technical Considerations

### UTF-16 Index Handling
PyICU uses UTF-16 indices internally. We must:
- Use icu.UnicodeString for break iterators
- Convert indices properly for Python string slicing
- Test thoroughly with non-BMP characters

### Error Handling Strategy
- Wrap ICU errors in custom Python exceptions
- Provide clear error messages
- Maintain exception hierarchy for specific handling

### Performance Optimization
- Cache frequently used objects (e.g., break iterators)
- Minimize string conversions between Python and ICU
- Profile critical paths

### Thread Safety
- Document thread safety of wrapped objects
- Avoid global state where possible
- Consider thread-local storage for caches

## API Design Patterns

### Factory Pattern
```python
locale = uicu.Locale('de-DE')
collator = locale.get_collator()
formatter = locale.get_date_formatter()
```

### Functional Shortcuts
```python
# Direct functions for common operations
uicu.sort(['a', 'ä', 'b'], locale='de-DE')
uicu.graphemes('👨‍👩‍👧‍👦')  # Family emoji as one grapheme
```

### Iterator Protocol
```python
# All segmenters return iterators
for word in uicu.words(text, locale='th-TH'):
    process(word)
```

### Context Managers (where appropriate)
```python
with uicu.locale_context('fr-FR'):
    # Operations use French locale by default
    pass
```

## Testing Strategy

1. **Unit Tests**: Test each function/method in isolation
2. **Integration Tests**: Test interaction between components
3. **Locale Tests**: Test with various locales (LTR, RTL, CJK)
4. **Edge Cases**: Non-BMP characters, empty strings, invalid inputs
5. **Performance Tests**: Benchmark against raw PyICU

## Documentation Plan

1. **API Reference**: Auto-generated from docstrings
2. **User Guide**: Tutorial-style introduction
3. **Migration Guide**: From PyICU to uicu
4. **Examples**: Common use cases with code
5. **Architecture**: Technical details for contributors

## Success Criteria

1. All major PyICU functionality accessible via Pythonic API
2. Comprehensive test coverage (>95%)
3. Performance overhead <10% vs raw PyICU
4. Clear documentation with examples
5. Successful handling of complex Unicode (emoji, RTL, etc.)

## Future Enhancements

- Regex wrapper with Unicode properties
- Bidirectional text support
- Calendar systems
- Unicode security (confusables, etc.)
- Integration with Python's locale module