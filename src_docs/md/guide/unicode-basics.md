---
# this_file: src_docs/md/guide/unicode-basics.md
title: Unicode Basics
description: Essential Unicode concepts and UICU's approach
---

# Unicode Basics

Understanding Unicode is essential for effective text processing. This chapter covers Unicode fundamentals and how UICU simplifies complex Unicode operations.

## What is Unicode?

Unicode is a computing standard that assigns unique numbers (code points) to characters from all writing systems worldwide. It enables consistent representation of text across different platforms and languages.

### Key Concepts

**Code Point**: A unique number assigned to each character
```python
import uicu

# Character 'A' has code point U+0041
char_a = uicu.Char('A')
print(f"Code point: U+{char_a.code_point:04X}")  # U+0041
print(f"Decimal: {char_a.code_point}")           # 65
```

**Encoding**: How code points are stored as bytes
```python
# UTF-8 encoding of 'A'
text = 'A'
utf8_bytes = text.encode('utf-8')
print(f"UTF-8 bytes: {utf8_bytes}")  # b'A'

# UTF-8 encoding of emoji
emoji = '🌍'
emoji_bytes = emoji.encode('utf-8')
print(f"Emoji UTF-8: {emoji_bytes}")  # b'\xf0\x9f\x8c\x8d'
```

## Unicode Structure

### Planes and Blocks

Unicode is organized into 17 planes, each containing 65,536 code points:

```python
# Basic Multilingual Plane (BMP) - Plane 0
latin_a = uicu.Char('A')
print(f"Plane: {latin_a.plane}")  # 0
print(f"Block: {latin_a.block}")  # Basic Latin

# Supplementary Multilingual Plane - Plane 1
emoji = uicu.Char('🎯')
print(f"Plane: {emoji.plane}")  # 1
print(f"Block: {emoji.block}")  # Miscellaneous Symbols and Pictographs
```

### Character Categories

Unicode defines general categories for all characters:

```python
# Major categories
examples = {
    'Lu': 'A',      # Letter, Uppercase
    'Ll': 'a',      # Letter, Lowercase
    'Nd': '5',      # Number, Decimal digit
    'Sc': '$',      # Symbol, Currency
    'Po': '.',      # Punctuation, Other
    'Sm': '+',      # Symbol, Math
    'So': '🎯',     # Symbol, Other (emoji)
    'Mn': '\u0301', # Mark, Nonspacing (combining acute accent)
}

for category, char in examples.items():
    c = uicu.Char(char)
    print(f"{char} ({c.name}): {c.category}")
```

## Scripts and Writing Systems

Unicode organizes characters by script (writing system):

```python
# Different scripts
scripts = {
    'Latin': 'Hello',
    'Cyrillic': 'Привет',
    'Greek': 'Γεια',
    'Arabic': 'مرحبا',
    'Hebrew': 'שלום',
    'Devanagari': 'नमस्ते',
    'Han': '你好',
    'Hiragana': 'こんにちは',
    'Katakana': 'コンニチハ',
}

for script_name, text in scripts.items():
    first_char = uicu.Char(text[0])
    print(f"{script_name}: {text} (Script: {first_char.script})")
```

## Normalization

Unicode allows multiple representations of the same text. Normalization ensures consistent representation:

### Normalization Forms

```python
# Different representations of "café"
text1 = "café"           # é as single character (U+00E9)
text2 = "cafe\u0301"     # e + combining acute accent (U+0065 + U+0301)

print(f"Text 1: {repr(text1)} (length: {len(text1)})")
print(f"Text 2: {repr(text2)} (length: {len(text2)})")
print(f"Equal? {text1 == text2}")  # False - different representations

# Normalize to NFC (Canonical Decomposition, then Canonical Composition)
nfc1 = uicu.normalize(text1, 'NFC')
nfc2 = uicu.normalize(text2, 'NFC')
print(f"NFC equal? {nfc1 == nfc2}")  # True

# Normalize to NFD (Canonical Decomposition)
nfd1 = uicu.normalize(text1, 'NFD')
nfd2 = uicu.normalize(text2, 'NFD')
print(f"NFD form: {repr(nfd1)}")  # Both become 'cafe\u0301'
```

### When to Use Each Form

- **NFC**: Default for most applications (composed form)
- **NFD**: Useful for text analysis and searching
- **NFKC**: Compatibility composition (converts similar characters)
- **NFKD**: Compatibility decomposition

```python
# NFKC example - compatibility normalization
text_with_ligature = "ﬁle"  # Contains fi ligature (U+FB01)
nfc_result = uicu.normalize(text_with_ligature, 'NFC')
nfkc_result = uicu.normalize(text_with_ligature, 'NFKC')

print(f"Original: {text_with_ligature}")
print(f"NFC: {nfc_result}")        # Keeps ligature
print(f"NFKC: {nfkc_result}")      # Converts to "file"
```

## Case Handling

Unicode case handling is complex due to language-specific rules:

```python
# Simple case conversion
text = "Hello World"
print(f"Upper: {uicu.upper(text)}")
print(f"Lower: {uicu.lower(text)}")
print(f"Title: {uicu.title(text)}")

# Case folding for comparison
print(f"Case fold: {uicu.case_fold(text)}")

# Language-specific rules
turkish_i = "İstanbul"  # Turkish capital I with dot
print(f"Turkish lower: {uicu.lower(turkish_i, locale='tr-TR')}")  # istanbul
print(f"English lower: {uicu.lower(turkish_i, locale='en-US')}")  # i̇stanbul

# German sharp s
german_text = "Straße"
print(f"German upper: {uicu.upper(german_text, locale='de-DE')}")  # STRASSE
```

## Grapheme Clusters

What users perceive as "characters" may be multiple Unicode code points:

```python
# Complex grapheme examples
examples = [
    "é",                    # Single character
    "e\u0301",             # e + combining acute
    "👨‍👩‍👧‍👦",              # Family emoji (multiple code points)
    "🇺🇸",                   # Flag emoji (regional indicators)
    "नमस्ते",                # Devanagari with combining marks
]

for text in examples:
    code_points = [ord(c) for c in text]
    graphemes = list(uicu.graphemes(text))
    
    print(f"Text: {text}")
    print(f"  Code points: {len(code_points)} {[f'U+{cp:04X}' for cp in code_points]}")
    print(f"  Graphemes: {len(graphemes)} {graphemes}")
    print()
```

## Bidirectional Text

Text direction is handled automatically by UICU:

```python
# Mixed text with different directions
mixed_text = "Hello שלום مرحبا World"

# Analyze text direction
for char in mixed_text:
    if char.strip():  # Skip spaces
        c = uicu.Char(char)
        print(f"{char}: {c.bidi_class}")

# Get overall text direction
direction = uicu.get_base_direction(mixed_text)
print(f"Base direction: {direction}")  # LTR, RTL, or Mixed
```

## Unicode Properties

UICU provides access to rich Unicode character properties:

```python
# Comprehensive character analysis
def analyze_char(char):
    c = uicu.Char(char)
    return {
        'character': char,
        'name': c.name,
        'code_point': f'U+{c.code_point:04X}',
        'category': c.category,
        'script': c.script,
        'block': c.block,
        'is_letter': c.is_letter,
        'is_digit': c.is_digit,
        'is_punctuation': c.is_punctuation,
        'is_symbol': c.is_symbol,
        'is_whitespace': c.is_whitespace,
        'numeric_value': c.numeric_value,
        'bidi_class': c.bidi_class,
    }

# Analyze different character types
characters = ['A', '5', '€', '🎯', ' ', '\n', 'ñ']
for char in characters:
    info = analyze_char(char)
    print(f"{info['character']}: {info['name']} ({info['category']})")
```

## Text Comparison

Unicode-aware text comparison considers normalization and case:

```python
# Create comparison function
def unicode_equal(text1, text2, case_sensitive=True, normalize=True):
    if normalize:
        text1 = uicu.normalize(text1, 'NFC')
        text2 = uicu.normalize(text2, 'NFC')
    
    if not case_sensitive:
        text1 = uicu.case_fold(text1)
        text2 = uicu.case_fold(text2)
    
    return text1 == text2

# Test comparisons
test_pairs = [
    ("café", "cafe\u0301"),      # Different normalization
    ("Hello", "HELLO"),          # Different case
    ("İstanbul", "istanbul"),    # Turkish I
    ("Straße", "STRASSE"),       # German sharp s
]

for text1, text2 in test_pairs:
    print(f"'{text1}' vs '{text2}':")
    print(f"  Exact: {text1 == text2}")
    print(f"  Unicode equal: {unicode_equal(text1, text2)}")
    print(f"  Case insensitive: {unicode_equal(text1, text2, case_sensitive=False)}")
    print()
```

## Best Practices

### 1. Always Normalize Input

```python
def process_user_input(text):
    # Normalize to NFC for consistent representation
    normalized = uicu.normalize(text, 'NFC')
    # Strip leading/trailing whitespace
    return normalized.strip()
```

### 2. Use Proper Case Handling

```python
def case_insensitive_compare(text1, text2):
    # Use case folding, not just lower()
    return uicu.case_fold(text1) == uicu.case_fold(text2)
```

### 3. Handle Grapheme Boundaries

```python
def truncate_text(text, max_length):
    # Truncate by graphemes, not code points
    graphemes = list(uicu.graphemes(text))
    if len(graphemes) <= max_length:
        return text
    return ''.join(graphemes[:max_length])
```

### 4. Validate Text Input

```python
def is_valid_text(text):
    # Check for proper Unicode
    try:
        # Ensure it's valid Unicode
        text.encode('utf-8').decode('utf-8')
        # Check for control characters (except whitespace)
        for char in text:
            c = uicu.Char(char)
            if c.category.startswith('C') and not c.is_whitespace:
                return False
        return True
    except UnicodeError:
        return False
```

## Performance Considerations

UICU optimizes Unicode operations:

```python
import time

# Efficient character analysis with caching
def benchmark_char_analysis():
    text = "Hello, 世界! 🌍" * 1000
    
    start = time.time()
    for char in text:
        c = uicu.Char(char)  # Cached internally
        _ = c.category
    end = time.time()
    
    print(f"Analyzed {len(text)} characters in {end - start:.3f}s")

benchmark_char_analysis()
```

## Next Steps

Now that you understand Unicode basics:

1. **[Character Properties](character-properties.md)** - Deep dive into character analysis
2. **[Text Collation](text-collation.md)** - Unicode-aware sorting and comparison
3. **[Text Segmentation](text-segmentation.md)** - Breaking text properly
4. **[Locale Management](locale-management.md)** - Handling international text

!!! info "Unicode Version"
    UICU supports Unicode 15.0, which includes over 149,000 characters from 161 scripts.

Ready to explore character properties in detail? Continue to [Character Properties](character-properties.md)!