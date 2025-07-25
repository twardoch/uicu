# Unicode Basics

Understanding Unicode is essential for modern text processing. This guide covers fundamental Unicode concepts and how UICU helps you work with them.

## What is Unicode?

Unicode is a universal character encoding standard that assigns a unique number (code point) to every character from all writing systems in the world.

### Key Concepts

#### Code Points
A code point is a unique number assigned to each character:
- Written as `U+XXXX` (e.g., `U+0041` for 'A')
- Range from `U+0000` to `U+10FFFF`
- Over 140,000 characters defined

```python
import uicu

# Work with code points
char = uicu.Char('A')
print(f"Character: {char.value}")
print(f"Code point: U+{ord(char.value):04X}")  # U+0041
print(f"Name: {char.name}")  # LATIN CAPITAL LETTER A
```

#### Code Units vs. Code Points
- **Code Point**: The Unicode number for a character
- **Code Unit**: How it's stored in a specific encoding (UTF-8, UTF-16)

```python
# A single character can have multiple code units
text = "🎉"  # Party popper emoji
print(f"Character: {text}")
print(f"Code point: U+{ord(text):04X}")  # U+1F389
print(f"UTF-8 bytes: {len(text.encode('utf-8'))}")  # 4 bytes
print(f"UTF-16 code units: {len(text.encode('utf-16-le'))//2}")  # 2 units
```

#### Grapheme Clusters
A grapheme cluster is what users perceive as a single character:

```python
# Some "characters" are multiple code points
family = "👨‍👩‍👧‍👦"  # Family emoji
print(f"String length: {len(family)}")  # 7 code points!
print(f"Grapheme clusters: {list(uicu.graphemes(family))}")  # ['👨‍👩‍👧‍👦']

# Regional indicators form flag emojis
flag = "🇺🇸"  # US flag
print(f"Code points: {len(flag)}")  # 2
print(f"Graphemes: {list(uicu.graphemes(flag))}")  # ['🇺🇸']
```

## Unicode Properties

Every Unicode character has multiple properties:

### General Categories
Characters are classified into categories:

```python
# Explore character categories
chars = ['A', '5', '$', ' ', '你', '🎉']
for char in chars:
    c = uicu.Char(char)
    print(f"{char}: {c.category} - {c.category_name}")
```

Common categories:
- `Lu`: Letter, uppercase
- `Ll`: Letter, lowercase
- `Nd`: Number, decimal digit
- `Sc`: Symbol, currency
- `Zs`: Separator, space
- `So`: Symbol, other

### Scripts and Blocks

#### Scripts
A script is a writing system:

```python
# Detect scripts in text
texts = ['Hello', 'Привет', 'こんにちは', '你好', 'مرحبا']
for text in texts:
    script = uicu.detect_script(text)
    print(f"{text}: {script}")
```

Common scripts:
- `Latn`: Latin
- `Cyrl`: Cyrillic
- `Arab`: Arabic
- `Hani`: Han (Chinese)
- `Jpan`: Japanese

#### Blocks
Blocks are contiguous ranges of code points:

```python
# Check character blocks
chars = ['A', 'Ω', '中', '🎉', '𝓐']
for char in chars:
    c = uicu.Char(char)
    print(f"{char}: {c.block}")
```

## Text Encoding

### UTF-8, UTF-16, and UTF-32

Different ways to encode Unicode code points as bytes:

```python
text = "Hello 世界 🌍"

# UTF-8: Variable width (1-4 bytes per character)
utf8 = text.encode('utf-8')
print(f"UTF-8: {len(utf8)} bytes")

# UTF-16: Variable width (2 or 4 bytes per character)
utf16 = text.encode('utf-16-le')
print(f"UTF-16: {len(utf16)} bytes")

# UTF-32: Fixed width (4 bytes per character)
utf32 = text.encode('utf-32-le')
print(f"UTF-32: {len(utf32)} bytes")
```

### Byte Order Mark (BOM)

The BOM indicates byte order in UTF-16/32:

```python
# BOM examples
text = "Hello"
utf16_be = text.encode('utf-16-be')  # Big-endian, no BOM
utf16 = text.encode('utf-16')  # With BOM

print(f"UTF-16-BE: {utf16_be.hex()}")
print(f"UTF-16 with BOM: {utf16.hex()}")
```

## Normalization

Unicode provides multiple ways to represent the same text:

```python
# Composed vs. decomposed forms
composed = "é"  # Single code point U+00E9
decomposed = "é"  # e (U+0065) + combining acute (U+0301)

print(f"Look the same? {composed == decomposed}")  # False!
print(f"Same length? {len(composed)} vs {len(decomposed)}")  # 1 vs 2

# Use normalization to compare correctly
import unicodedata
nfc_composed = unicodedata.normalize('NFC', composed)
nfc_decomposed = unicodedata.normalize('NFC', decomposed)
print(f"After NFC: {nfc_composed == nfc_decomposed}")  # True
```

Normalization forms:
- **NFC**: Canonical composition (preferred for storage)
- **NFD**: Canonical decomposition
- **NFKC**: Compatibility composition
- **NFKD**: Compatibility decomposition

## Bidirectional Text

Some scripts are written right-to-left:

```python
# Check text directionality
texts = ['Hello', 'مرحبا', 'שלום', 'Hello مرحبا mixed']
for text in texts:
    # Check first character's direction
    if text:
        char = uicu.Char(text[0])
        print(f"{text}: {char.bidirectional}")
```

Bidirectional categories:
- `L`: Left-to-right (Latin, Chinese)
- `R`: Right-to-left (Arabic, Hebrew)
- `AL`: Arabic letter
- `EN`: European number
- `AN`: Arabic number

## Case Mapping

Unicode case operations are locale-sensitive:

```python
# Simple case mapping
text = "Hello World"
trans_upper = uicu.Transliterator('Upper')
trans_lower = uicu.Transliterator('Lower')

print(trans_upper.transliterate(text))  # HELLO WORLD
print(trans_lower.transliterate(text))  # hello world

# Turkish has special case rules
turkish_i = "i"
# In Turkish, lowercase 'i' uppercases to 'İ' (with dot)
# and 'I' lowercases to 'ı' (without dot)
```

## Combining Characters

Some characters modify the preceding character:

```python
# Combining characters
base = "e"
combining_acute = "\u0301"  # Combining acute accent
combined = base + combining_acute

print(f"Base: {base}")
print(f"Combined: {combined}")  # é
print(f"Length: {len(combined)}")  # 2 code points
print(f"Graphemes: {list(uicu.graphemes(combined))}")  # ['é']
```

## Private Use Areas

Unicode reserves areas for private use:
- U+E000 to U+F8FF (BMP)
- U+F0000 to U+FFFFD (Plane 15)
- U+100000 to U+10FFFD (Plane 16)

```python
# Check if character is in private use area
private_char = '\uE000'
c = uicu.Char(private_char)
print(f"Category: {c.category}")  # Co (Other, private use)
```

## Surrogate Pairs

UTF-16 uses surrogate pairs for characters beyond U+FFFF:

```python
# Emoji uses surrogate pairs in UTF-16
emoji = "😀"
utf16 = emoji.encode('utf-16-le')
print(f"UTF-16 bytes: {utf16.hex()}")
print(f"Surrogate pair: {len(utf16) == 4}")  # True
```

## Unicode Versions

Unicode is regularly updated with new characters:

```python
# Check Unicode data version
import icu
print(f"ICU Unicode version: {icu.UNICODE_VERSION}")
```

## Practical Examples

### Validating Unicode Text

```python
def analyze_unicode_text(text: str):
    """Analyze Unicode properties of text."""
    print(f"Analyzing: {text!r}")
    print(f"Code points: {len(text)}")
    print(f"Grapheme clusters: {len(list(uicu.graphemes(text)))}")
    
    # Analyze each character
    for i, char in enumerate(text[:10]):  # First 10 chars
        try:
            c = uicu.Char(char)
            print(f"  {char!r}: {c.category} - {c.name}")
        except uicu.UICUError:
            print(f"  {char!r}: Invalid character")
    
    # Detect scripts
    script = uicu.detect_script(text)
    if script:
        print(f"Primary script: {script}")

# Test with various texts
analyze_unicode_text("Hello, 世界! 🌍")
analyze_unicode_text("مرحبا بالعالم")
analyze_unicode_text("🏳️‍🌈🏳️‍⚧️")  # Flag emojis with ZWJ sequences
```

### Handling Mixed Scripts

```python
def split_by_script(text: str):
    """Split text into runs of same script."""
    if not text:
        return []
    
    runs = []
    current_run = []
    current_script = None
    
    for char in text:
        script = uicu.script(char)
        # Ignore common/inherited scripts
        if script in ('Zyyy', 'Zinh'):
            if current_run:
                current_run.append(char)
            continue
            
        if script != current_script:
            if current_run:
                runs.append((''.join(current_run), current_script))
            current_run = [char]
            current_script = script
        else:
            current_run.append(char)
    
    if current_run:
        runs.append((''.join(current_run), current_script))
    
    return runs

# Example with mixed scripts
mixed = "Hello 你好 مرحبا"
runs = split_by_script(mixed)
for text, script in runs:
    print(f"{text!r} -> {script}")
```

## Best Practices

1. **Always consider grapheme clusters** when counting user-visible characters
2. **Use normalization** before comparing strings
3. **Be aware of locale differences** in case mapping
4. **Handle surrogate pairs** properly in UTF-16 environments
5. **Test with diverse Unicode data** including emoji and combining characters

## Next Steps

- Learn about [Character Properties](character-properties.md) in detail
- Understand [Text Segmentation](text-segmentation.md) for proper text breaking
- Explore [Locale Management](locale-management.md) for internationalization