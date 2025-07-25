# Character Properties

UICU provides comprehensive access to Unicode character properties, combining data from PyICU and fontTools for the most complete character information available.

## The Char Class

The `Char` class is your gateway to Unicode character properties:

```python
import uicu

# Create a Char object
char = uicu.Char('A')

# Access basic properties
print(f"Character: {char.value}")
print(f"Name: {char.name}")
print(f"Category: {char.category}")
print(f"Script: {char.script}")
```

### Creating Char Objects

```python
# From a single character
char1 = uicu.Char('€')

# From Unicode escape
char2 = uicu.Char('\u20AC')  # Also Euro sign

# From code point
char3 = uicu.Char(chr(0x20AC))  # Also Euro sign

# Error handling for invalid input
try:
    char4 = uicu.Char('AB')  # Error: multi-character string
except uicu.UICUError as e:
    print(f"Error: {e}")
```

## Character Categories

Unicode categorizes every character:

```python
# Explore different categories
test_chars = [
    ('A', 'Uppercase letter'),
    ('a', 'Lowercase letter'),
    ('5', 'Decimal number'),
    ('Ⅴ', 'Roman numeral'),
    ('$', 'Currency symbol'),
    (' ', 'Space'),
    ('_', 'Connector punctuation'),
    ('🎉', 'Other symbol'),
    ('\n', 'Line separator'),
    ('\u200B', 'Zero-width space'),
]

for char, desc in test_chars:
    c = uicu.Char(char)
    print(f"{desc:20} {char!r:>6} -> {c.category} ({c.category_name})")
```

### Category Groups

Categories follow a two-letter system:
- First letter: Major category (L=Letter, N=Number, etc.)
- Second letter: Subcategory (u=uppercase, d=decimal, etc.)

```python
# Check category groups
def analyze_category(char: str):
    c = uicu.Char(char)
    cat = c.category
    
    major_categories = {
        'L': 'Letter',
        'M': 'Mark',
        'N': 'Number',
        'P': 'Punctuation',
        'S': 'Symbol',
        'Z': 'Separator',
        'C': 'Other',
    }
    
    major = cat[0]
    print(f"{char!r}: {cat} - {major_categories.get(major, 'Unknown')} ({c.category_name})")

# Examples
for char in ['A', 'à', '5', '½', '!', '€', ' ', '\n', '\u0301']:
    analyze_category(char)
```

## Scripts and Writing Systems

### Script Detection

```python
# Detect scripts in various languages
samples = [
    ('English', 'Hello World'),
    ('Greek', 'Γειά σου Κόσμε'),
    ('Russian', 'Привет мир'),
    ('Arabic', 'مرحبا بالعالم'),
    ('Hebrew', 'שלום עולם'),
    ('Chinese', '你好世界'),
    ('Japanese', 'こんにちは世界'),
    ('Thai', 'สวัสดีชาวโลก'),
    ('Emoji', '🌍🌎🌏'),
]

for lang, text in samples:
    script = uicu.detect_script(text)
    print(f"{lang:10} {text:20} -> Script: {script}")
```

### Script Properties

```python
# Get detailed script information
def analyze_script(char: str):
    c = uicu.Char(char)
    print(f"Character: {char}")
    print(f"  Script: {c.script}")
    print(f"  Script name: {c.script_name}")
    print(f"  Script direction: {c.script_direction}")
    
    # Script extensions (characters used in multiple scripts)
    extensions = c.script_extensions
    if extensions and len(extensions) > 1:
        print(f"  Also used in: {', '.join(extensions)}")

# Examples
for char in ['A', 'Ω', '中', 'あ', 'א', '᠀', '🙂']:
    analyze_script(char)
    print()
```

## Numeric Properties

Unicode includes various numeric representations:

```python
# Explore numeric characters
numeric_chars = [
    ('5', 'ASCII digit'),
    ('५', 'Devanagari digit'),
    ('๕', 'Thai digit'),
    ('Ⅴ', 'Roman numeral'),
    ('⅚', 'Fraction'),
    ('³', 'Superscript'),
    ('½', 'Vulgar fraction'),
    ('万', 'CJK ideograph (10,000)'),
]

for char, desc in numeric_chars:
    c = uicu.Char(char)
    print(f"{desc:20} {char} ->", end='')
    print(f" decimal: {c.decimal}", end='')
    print(f" digit: {c.digit}", end='')
    print(f" numeric: {c.numeric}")
```

### Working with Numeric Values

```python
# Convert numeric characters to values
def parse_numeric_string(text: str) -> float:
    """Parse a string containing Unicode numeric characters."""
    total = 0
    for char in text:
        numeric = uicu.numeric(char)
        if numeric is not None:
            total = total * 10 + numeric
    return total

# Examples
print(parse_numeric_string("123"))      # ASCII
print(parse_numeric_string("१२३"))      # Devanagari
print(parse_numeric_string("๑๒๓"))      # Thai
```

## Bidirectional Properties

For handling right-to-left and mixed-direction text:

```python
# Analyze bidirectional properties
bidi_samples = [
    'Hello',          # Left-to-right
    'مرحبا',          # Right-to-left Arabic
    'שלום',           # Right-to-left Hebrew
    'Hello مرحبا',    # Mixed direction
    '123',            # Numbers
    '١٢٣',            # Arabic-Indic digits
]

for text in bidi_samples:
    print(f"\n{text!r}:")
    for char in text:
        c = uicu.Char(char)
        print(f"  {char!r}: {c.bidirectional} ({c.bidirectional_name})")
```

### Bidirectional Categories

Common bidirectional categories:
- `L`: Strong left-to-right
- `R`: Strong right-to-left
- `AL`: Arabic letter (right-to-left)
- `EN`: European number
- `AN`: Arabic number
- `WS`: Whitespace
- `ON`: Other neutral

## Case and Casing

```python
# Explore case properties
case_samples = [
    'A', 'a',        # Simple case
    'Σ', 'σ', 'ς',   # Greek with final sigma
    'İ', 'i',        # Turkish
    'ß',             # German sharp s
    'ﬁ',             # Ligature
    '𝓐',             # Mathematical alphanumeric
]

for char in case_samples:
    c = uicu.Char(char)
    print(f"{char}: {c.category}", end='')
    
    # Check case properties using Python's methods
    if char.isupper():
        print(" [UPPER]", end='')
    if char.islower():
        print(" [LOWER]", end='')
    if char.istitle():
        print(" [TITLE]", end='')
    print()
```

## Blocks and Ranges

Unicode organizes characters into contiguous blocks:

```python
# Explore different Unicode blocks
block_samples = [
    'A',      # Basic Latin
    'É',      # Latin-1 Supplement
    'Ω',      # Greek and Coptic
    'Я',      # Cyrillic
    'म',      # Devanagari
    '中',     # CJK Unified Ideographs
    '🎉',     # Miscellaneous Symbols and Pictographs
    '𝔸',      # Mathematical Alphanumeric Symbols
    '🏴‍☠️',      # Emoji with modifiers
]

for char in block_samples:
    c = uicu.Char(char)
    print(f"{char!r}: {c.block}")
```

## Combining and Modifier Characters

```python
# Work with combining characters
base_char = 'e'
combining_marks = [
    '\u0301',  # Combining acute accent
    '\u0300',  # Combining grave accent
    '\u0302',  # Combining circumflex accent
    '\u0303',  # Combining tilde
    '\u0308',  # Combining diaeresis
]

print("Base + Combining = Result")
for mark in combining_marks:
    combined = base_char + mark
    c = uicu.Char(mark)
    print(f"e + {c.name:30} = {combined}")

# Check combining class
for mark in combining_marks:
    c = uicu.Char(mark)
    print(f"{mark!r}: Combining class {c.combining}")
```

## Emoji and Special Characters

### Emoji Properties

```python
# Analyze emoji characters
emoji_samples = [
    '😀',      # Basic emoji
    '👍',      # Hand emoji
    '👍🏽',     # With skin tone modifier
    '🏳️‍🌈',    # Rainbow flag (multiple components)
    '👨‍👩‍👧‍👦',  # Family (ZWJ sequence)
    '🇺🇸',     # Flag (regional indicators)
    '™️',      # Text vs emoji presentation
]

for emoji in emoji_samples:
    print(f"\n{emoji!r} ({len(emoji)} code points):")
    # Analyze first code point
    if emoji:
        try:
            c = uicu.Char(emoji[0])
            print(f"  First char: {c.name}")
            print(f"  Category: {c.category}")
            print(f"  Script: {c.script}")
        except uicu.UICUError as e:
            print(f"  Error: {e}")
    
    # Show grapheme clusters
    graphemes = list(uicu.graphemes(emoji))
    print(f"  Grapheme clusters: {len(graphemes)}")
```

### Zero-Width Characters

```python
# Explore zero-width and invisible characters
invisible_chars = [
    ('\u200B', 'ZERO WIDTH SPACE'),
    ('\u200C', 'ZERO WIDTH NON-JOINER'),
    ('\u200D', 'ZERO WIDTH JOINER'),
    ('\uFEFF', 'ZERO WIDTH NO-BREAK SPACE (BOM)'),
    ('\u2060', 'WORD JOINER'),
    ('\u00AD', 'SOFT HYPHEN'),
]

for char, name in invisible_chars:
    c = uicu.Char(char)
    print(f"{name:35} U+{ord(char):04X} Cat: {c.category}")
    
    # Show effect in strings
    test = f"AB{char}CD"
    print(f"  'AB' + char + 'CD' = {test!r} (len={len(test)})")
```

## Mirroring and Paired Characters

```python
# Characters that mirror in RTL contexts
mirrored_chars = [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('<', '>'),
    ('«', '»'),
]

print("Character mirroring in RTL contexts:")
for left, right in mirrored_chars:
    c_left = uicu.Char(left)
    c_right = uicu.Char(right)
    print(f"{left} ({c_left.mirrored}) <-> {right} ({c_right.mirrored})")
```

## Practical Examples

### Character Validation

```python
def validate_identifier(name: str) -> bool:
    """Check if string is valid Unicode identifier."""
    if not name:
        return False
    
    # First character must be ID_Start
    first = name[0]
    if not (first.isalpha() or first == '_'):
        return False
    
    # Rest must be ID_Continue
    for char in name[1:]:
        if not (char.isalnum() or char == '_'):
            return False
    
    return True

# Test identifier validation
test_names = [
    'valid_name',
    'name123',
    '123invalid',  # Starts with digit
    'ñame',        # Non-ASCII letter
    'name-with-dash',  # Invalid character
    '名前',         # CJK characters
]

for name in test_names:
    valid = validate_identifier(name)
    print(f"{name:15} -> {'Valid' if valid else 'Invalid'}")
```

### Text Classification

```python
def classify_text(text: str) -> dict:
    """Classify text by character types."""
    stats = {
        'letters': 0,
        'digits': 0,
        'spaces': 0,
        'punctuation': 0,
        'symbols': 0,
        'other': 0,
        'scripts': set(),
    }
    
    for char in text:
        c = uicu.Char(char)
        cat = c.category
        
        # Count by major category
        if cat.startswith('L'):
            stats['letters'] += 1
        elif cat.startswith('N'):
            stats['digits'] += 1
        elif cat.startswith('Z'):
            stats['spaces'] += 1
        elif cat.startswith('P'):
            stats['punctuation'] += 1
        elif cat.startswith('S'):
            stats['symbols'] += 1
        else:
            stats['other'] += 1
        
        # Track scripts
        script = c.script
        if script not in ('Zyyy', 'Zinh', 'Zzzz'):
            stats['scripts'].add(script)
    
    stats['scripts'] = list(stats['scripts'])
    return stats

# Analyze sample text
sample = "Hello, 世界! 123 🌍 #Unicode"
stats = classify_text(sample)
print(f"Text: {sample!r}")
for key, value in stats.items():
    print(f"  {key}: {value}")
```

### Security: Confusable Detection

```python
def find_confusables(text: str) -> list:
    """Find potentially confusable characters."""
    # Common confusable pairs
    confusables = {
        'o': ['0', 'о', 'ο'],  # Latin o, zero, Cyrillic o, Greek omicron
        'l': ['1', 'I', '|', 'ı'],  # Lowercase L, one, uppercase i, pipe, dotless i
        'a': ['а', 'ɑ', '@'],  # Latin a, Cyrillic a, turned a, at sign
    }
    
    found = []
    for char in text.lower():
        if char in confusables:
            for conf in confusables[char]:
                if conf in text:
                    found.append((char, conf))
    
    return found

# Check for confusables
test_strings = [
    "password",
    "p@ssw0rd",  # Common substitutions
    "раssword",  # Cyrillic 'а'
]

for text in test_strings:
    print(f"\n{text!r}:")
    confusables = find_confusables(text)
    if confusables:
        print("  Potential confusables found:")
        for orig, conf in confusables:
            c = uicu.Char(conf)
            print(f"    '{orig}' vs '{conf}' ({c.name})")
```

## Performance Tips

1. **Cache Char objects** when analyzing the same character repeatedly
2. **Use functional API** for one-off property access: `uicu.name('A')`
3. **Batch operations** when analyzing multiple characters
4. **Check category prefix** instead of full category when appropriate

```python
# Performance comparison
import time

text = "Hello, 世界!" * 1000

# Method 1: Create Char objects (slower)
start = time.time()
for char in text:
    c = uicu.Char(char)
    _ = c.category
elapsed1 = time.time() - start

# Method 2: Use functional API (faster)
start = time.time()
for char in text:
    _ = uicu.category(char)
elapsed2 = time.time() - start

print(f"Char objects: {elapsed1:.3f}s")
print(f"Functional API: {elapsed2:.3f}s")
print(f"Speedup: {elapsed1/elapsed2:.1f}x")
```

## Next Steps

- Explore [Text Segmentation](text-segmentation.md) for breaking text properly
- Learn about [Locale Management](locale-management.md) for culture-aware processing
- Master [Text Collation](text-collation.md) for proper sorting