---
# this_file: src_docs/md/guide/character-properties.md
title: Character Properties
description: Rich character information and analysis
---

# Character Properties

UICU's `Char` class provides comprehensive access to Unicode character properties, making character analysis intuitive and powerful.

## The Char Class

The `Char` class wraps a single Unicode character with rich metadata:

```python
import uicu

# Create character instances
letter_a = uicu.Char('A')
euro_sign = uicu.Char('€')
emoji = uicu.Char('🎯')
combining_accent = uicu.Char('\u0301')  # Combining acute accent

print(f"Letter: {letter_a.name}")           # LATIN CAPITAL LETTER A
print(f"Currency: {euro_sign.name}")        # EURO SIGN
print(f"Emoji: {emoji.name}")               # DIRECT HIT
print(f"Combining: {combining_accent.name}") # COMBINING ACUTE ACCENT
```

## Basic Properties

### Code Point and Representation

```python
char = uicu.Char('€')

# Unicode code point
print(f"Code point: U+{char.code_point:04X}")  # U+20AC
print(f"Decimal: {char.code_point}")           # 8364

# String representation
print(f"Character: {char}")                    # €
print(f"Repr: {repr(char)}")                   # Char('€')

# UTF-8 encoding
print(f"UTF-8: {char.utf8_bytes}")             # b'\xe2\x82\xac'
```

### Name and Aliases

```python
# Official Unicode name
print(f"Name: {char.name}")                    # EURO SIGN

# Name aliases (if any)
print(f"Aliases: {char.name_aliases}")         # []

# Age (Unicode version when added)
print(f"Age: {char.age}")                      # 2.1
```

## Character Categories

Unicode defines detailed character categories:

```python
# Major categories
examples = [
    ('A', 'Letter, Uppercase'),
    ('a', 'Letter, Lowercase'),  
    ('5', 'Number, Decimal digit'),
    ('€', 'Symbol, Currency'),
    ('.', 'Punctuation, Other'),
    ('+', 'Symbol, Math'),
    ('🎯', 'Symbol, Other'),
    (' ', 'Separator, Space'),
    ('\n', 'Other, Control'),
    ('\u0301', 'Mark, Nonspacing'),
]

for char_str, description in examples:
    char = uicu.Char(char_str)
    print(f"{char_str:>3} | {char.category:>2} | {description}")
```

### Category Hierarchy

```python
char = uicu.Char('A')

# Major category
print(f"Major category: {char.major_category}")  # L (Letter)

# Full category  
print(f"Category: {char.category}")              # Lu (Letter, uppercase)

# Category checks
print(f"Is letter: {char.is_letter}")           # True
print(f"Is uppercase: {char.is_uppercase}")     # True
print(f"Is lowercase: {char.is_lowercase}")     # False
```

### Common Category Checks

```python
def analyze_text_categories(text):
    """Analyze character categories in text"""
    categories = {}
    
    for char_str in text:
        char = uicu.Char(char_str)
        cat = char.category
        categories[cat] = categories.get(cat, 0) + 1
    
    return categories

# Analyze sample text
text = "Hello, 世界! 123 €50"
cats = analyze_text_categories(text)
for category, count in sorted(cats.items()):
    print(f"{category}: {count}")
```

## Scripts and Writing Systems

### Script Properties

```python
# Different scripts
examples = [
    ('A', 'Latin'),
    ('Α', 'Greek'), 
    ('А', 'Cyrillic'),
    ('א', 'Hebrew'),
    ('ا', 'Arabic'),
    ('あ', 'Hiragana'),
    ('漢', 'Han'),
    ('🎯', 'Common'),
]

for char_str, expected_script in examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | {char.script:>12} | {char.script_extensions}")
```

### Script Extensions

Some characters are used in multiple scripts:

```python
# Characters used in multiple scripts
multi_script_chars = [
    '\u0640',  # Arabic Tatweel (Arabic, Syriac, etc.)
    '\u3006',  # Ideographic closing mark (Hiragana, Katakana, Han)
    '0',       # Digits (Common, but used in many scripts)
]

for char_str in multi_script_chars:
    char = uicu.Char(char_str)
    print(f"{char.name}:")
    print(f"  Primary script: {char.script}")
    print(f"  Script extensions: {char.script_extensions}")
    print()
```

## Blocks and Planes

### Unicode Blocks

```python
# Characters from different blocks
block_examples = [
    ('A', 'Basic Latin'),
    ('€', 'Currency Symbols'),
    ('α', 'Greek and Coptic'),
    ('🎯', 'Miscellaneous Symbols and Pictographs'),
    ('𝕏', 'Mathematical Alphanumeric Symbols'),
]

for char_str, expected_block in block_examples:
    char = uicu.Char(char_str)
    print(f"{char_str:>2} | {char.block}")
```

### Planes

```python
# Characters from different planes
plane_examples = [
    ('A', 0, 'Basic Multilingual Plane'),          # U+0041
    ('𝕏', 1, 'Supplementary Multilingual Plane'),  # U+1D54F
    ('🎯', 1, 'Supplementary Multilingual Plane'), # U+1F3AF
]

for char_str, expected_plane, plane_name in plane_examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | Plane {char.plane} | {plane_name}")
    print(f"  Code point: U+{char.code_point:04X}")
```

## Numeric Properties

### Numeric Characters

```python
# Different types of numeric characters
numeric_examples = [
    '5',      # ASCII digit
    '½',      # Fraction
    'Ⅴ',      # Roman numeral
    '五',     # Chinese numeral
    '൫',      # Malayalam digit
]

for char_str in numeric_examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | {char.name}")
    print(f"  Is digit: {char.is_digit}")
    print(f"  Is numeric: {char.is_numeric}")
    print(f"  Numeric value: {char.numeric_value}")
    print(f"  Digit value: {char.digit_value}")
    print()
```

### Numeric Type

```python
def get_numeric_type(char_str):
    char = uicu.Char(char_str)
    if char.is_digit:
        return "Decimal digit"
    elif char.is_numeric:
        return "Numeric"
    else:
        return "Not numeric"

# Test various characters
test_chars = ['5', '½', 'Ⅴ', '五', 'A', '🎯']
for char_str in test_chars:
    print(f"{char_str}: {get_numeric_type(char_str)}")
```

## Case Properties

### Case Mapping

```python
# Case properties and mappings
case_examples = ['A', 'a', 'ß', 'İ', 'ﬃ']

for char_str in case_examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | {char.name}")
    print(f"  Is uppercase: {char.is_uppercase}")
    print(f"  Is lowercase: {char.is_lowercase}")
    print(f"  Is titlecase: {char.is_titlecase}")
    print(f"  Upper: {char.to_upper()}")
    print(f"  Lower: {char.to_lower()}")
    print(f"  Title: {char.to_title()}")
    print(f"  Case fold: {char.case_fold()}")
    print()
```

### Special Case Mappings

```python
# Characters with special case behavior
special_cases = [
    'ß',  # German sharp s
    'İ',  # Turkish capital I with dot
    'ﬃ', # Latin small ligature ffi
]

for char_str in special_cases:
    char = uicu.Char(char_str)
    print(f"{char_str} ({char.name}):")
    
    # Simple mappings
    print(f"  Simple upper: {char.simple_uppercase}")
    print(f"  Simple lower: {char.simple_lowercase}")
    print(f"  Simple title: {char.simple_titlecase}")
    
    # Full mappings (may be multiple characters)
    print(f"  Full upper: {char.to_upper()}")
    print(f"  Full lower: {char.to_lower()}")
    print(f"  Case fold: {char.case_fold()}")
    print()
```

## Bidirectional Properties

Text direction is crucial for proper display:

```python
# Bidirectional class examples
bidi_examples = [
    ('A', 'Left-to-Right'),
    ('א', 'Right-to-Left'),
    ('1', 'European Number'),
    (' ', 'White Space'),
    ('!', 'Other Neutral'),
    ('\u202D', 'Left-to-Right Override'),
]

for char_str, description in bidi_examples:
    char = uicu.Char(char_str)
    print(f"{char_str:>2} | {char.bidi_class:>3} | {description}")
```

### Mirrored Characters

Some characters have mirrored forms for RTL text:

```python
# Characters that are mirrored in RTL
mirrored_chars = ['(', ')', '[', ']', '<', '>', '{', '}']

for char_str in mirrored_chars:
    char = uicu.Char(char_str)
    print(f"{char_str} | Mirrored: {char.is_mirrored} | Mirror: {char.mirror}")
```

## Combining Properties

### Combining Marks

```python
# Combining characters
combining_examples = [
    '\u0300',  # Combining grave accent
    '\u0301',  # Combining acute accent
    '\u0302',  # Combining circumflex accent
    '\u0327',  # Combining cedilla
]

for char_str in combining_examples:
    char = uicu.Char(char_str)
    print(f"U+{char.code_point:04X} | {char.name}")
    print(f"  Combining class: {char.combining_class}")
    print(f"  Is combining: {char.is_combining}")
    print()

# Demonstrate combining
base = 'e'
accent = '\u0301'  # Combining acute accent
combined = base + accent
print(f"Base: {base}")
print(f"Combined: {combined}")
print(f"Length: {len(combined)} code points")
```

## Line Breaking Properties

Important for text layout:

```python
# Line breaking behavior
line_break_examples = [
    ('A', 'Alphabetic'),
    ('1', 'Numeric'),
    (' ', 'Space'),
    ('-', 'Hyphen'),
    ('!', 'Exclamation'),
    ('(', 'Open Punctuation'),
]

for char_str, description in line_break_examples:
    char = uicu.Char(char_str) 
    print(f"{char_str} | {char.line_break:>2} | {description}")
```

## Advanced Properties

### Decomposition

```python
# Character decomposition
decomp_examples = ['ﬁ', 'é', '½', '²']

for char_str in decomp_examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | {char.name}")
    print(f"  Has decomposition: {char.has_decomposition}")
    print(f"  Decomposition type: {char.decomposition_type}")
    print(f"  Decomposition: {char.decomposition}")
    print()
```

### East Asian Width

Important for terminal and monospace display:

```python
# East Asian width properties
width_examples = [
    ('A', 'Narrow'),
    ('あ', 'Wide'),
    ('ｱ', 'Halfwidth'),
    ('Ａ', 'Fullwidth'),
]

for char_str, description in width_examples:
    char = uicu.Char(char_str)
    print(f"{char_str} | {char.east_asian_width} | {description}")
```

## Practical Applications

### Text Validation

```python
def validate_identifier(name):
    """Validate a programming identifier"""
    if not name:
        return False, "Empty identifier"
    
    first_char = uicu.Char(name[0])
    if not (first_char.is_letter or first_char == '_'):
        return False, f"Invalid start character: {name[0]}"
    
    for i, char_str in enumerate(name[1:], 1):
        char = uicu.Char(char_str)
        if not (char.is_letter or char.is_digit or char_str == '_'):
            return False, f"Invalid character at position {i}: {char_str}"
    
    return True, "Valid identifier"

# Test identifiers
test_names = ['valid_name', '123invalid', 'name-with-dash', 'naïve', '_private']
for name in test_names:
    valid, message = validate_identifier(name)
    print(f"{name:15} | {message}")
```

### Character Set Analysis

```python
def analyze_character_set(text):
    """Analyze the character composition of text"""
    analysis = {
        'total_chars': len(text),
        'scripts': {},
        'categories': {},
        'combining_marks': 0,
        'control_chars': 0,
    }
    
    for char_str in text:
        char = uicu.Char(char_str)
        
        # Count scripts
        script = char.script
        analysis['scripts'][script] = analysis['scripts'].get(script, 0) + 1
        
        # Count categories
        category = char.category
        analysis['categories'][category] = analysis['categories'].get(category, 0) + 1
        
        # Special counts
        if char.is_combining:
            analysis['combining_marks'] += 1
        if char.category.startswith('C'):
            analysis['control_chars'] += 1
    
    return analysis

# Analyze mixed text
sample_text = "Hello, 世界! 🌍 Café naïve résumé"
result = analyze_character_set(sample_text)

print(f"Text: {sample_text}")
print(f"Total characters: {result['total_chars']}")
print(f"Scripts: {dict(sorted(result['scripts'].items()))}")
print(f"Categories: {dict(sorted(result['categories'].items()))}")
print(f"Combining marks: {result['combining_marks']}")
```

### Input Sanitization

```python
def sanitize_text_input(text, allow_categories=None):
    """Remove unwanted characters from user input"""
    if allow_categories is None:
        allow_categories = {'L', 'N', 'P', 'S', 'Z'}  # Letters, Numbers, Punct, Symbols, Separators
    
    sanitized = []
    removed = []
    
    for char_str in text:
        char = uicu.Char(char_str)
        major_cat = char.major_category
        
        if major_cat in allow_categories:
            sanitized.append(char_str)
        else:
            removed.append((char_str, char.name, char.category))
    
    return ''.join(sanitized), removed

# Test sanitization
test_input = "Hello\x00World\x01!\tTab\nNewline"
clean_text, removed_chars = sanitize_text_input(test_input)

print(f"Original: {repr(test_input)}")
print(f"Sanitized: {repr(clean_text)}")
print("Removed characters:")
for char, name, category in removed_chars:
    print(f"  {repr(char)} - {name} ({category})")
```

## Performance Tips

### Efficient Character Analysis

```python
import time

def benchmark_char_operations():
    """Benchmark character operations"""
    text = "Hello, 世界! 🌍" * 1000
    
    # Test character creation (cached)
    start = time.time()
    chars = [uicu.Char(c) for c in text]
    char_creation_time = time.time() - start
    
    # Test property access (cached)
    start = time.time()
    categories = [c.category for c in chars]
    property_access_time = time.time() - start
    
    print(f"Character creation: {char_creation_time:.4f}s for {len(text)} chars")
    print(f"Property access: {property_access_time:.4f}s for {len(text)} chars")
    print(f"Total: {char_creation_time + property_access_time:.4f}s")

benchmark_char_operations()
```

### Bulk Operations

```python
def bulk_analyze_scripts(text):
    """Efficiently analyze scripts in text"""
    script_counts = {}
    
    for char_str in text:
        char = uicu.Char(char_str)  # Cached internally
        script = char.script
        script_counts[script] = script_counts.get(script, 0) + 1
    
    return script_counts

# Analyze large text efficiently
large_text = "Hello, 世界! 🌍 " * 10000
scripts = bulk_analyze_scripts(large_text)
print(f"Scripts in {len(large_text)} characters: {scripts}")
```

## Next Steps

Now that you understand character properties:

1. **[Locale Management](locale-management.md)** - Handle international text
2. **[Text Collation](text-collation.md)** - Sort and compare text properly  
3. **[Text Segmentation](text-segmentation.md)** - Break text at proper boundaries
4. **[API Reference](../api/char.md)** - Complete Char class documentation

!!! tip "Character Caching"
    UICU automatically caches `Char` instances for better performance. Creating multiple `Char` objects for the same character is efficient.

Ready to explore locale-aware text processing? Continue to [Locale Management](locale-management.md)!