---
# this_file: src_docs/md/getting-started.md
title: Getting Started with UICU
description: Quick installation and your first UICU operations
---

# Getting Started with UICU

Get up and running with UICU in minutes! This guide walks you through installation and your first Unicode operations.

## Quick Installation

Install UICU using pip:

```bash
pip install uicu
```

!!! note "Prerequisites"
    UICU requires Python 3.8+ and automatically installs PyICU. See the [Installation](installation.md) guide for system-specific requirements.

## Your First UICU Program

Let's explore Unicode with a simple character analysis:

```python
import uicu

# Analyze a Unicode character
char = uicu.Char('🌍')
print(f"Character: {char}")
print(f"Name: {char.name}")
print(f"Category: {char.category}")
print(f"Script: {char.script}")
print(f"Block: {char.block}")
```

Output:
```
Character: 🌍
Name: EARTH GLOBE EUROPE-AFRICA
Category: So
Script: Common
Block: Miscellaneous Symbols and Pictographs
```

## Core Operations

### Character Properties

UICU makes character analysis intuitive:

```python
# Currency symbol
euro = uicu.Char('€')
print(f"{euro.name}: Category {euro.category}")
# EURO SIGN: Category Sc

# Letter with diacritics
a_acute = uicu.Char('á')
print(f"Base character: {a_acute.base_char}")
print(f"Has diacritics: {a_acute.has_diacritics}")
# Base character: a
# Has diacritics: True
```

### Locale-Aware Text Processing

Handle international text correctly:

```python
# German collation rules
german_collator = uicu.Collator('de-DE')
names = ['Müller', 'Mueller', 'Mahler']
sorted_names = german_collator.sort(names)
print(sorted_names)
# ['Mahler', 'Mueller', 'Müller'] (proper German order)

# Get locale information
locale = uicu.Locale('ja-JP')
print(f"Display name: {locale.display_name}")
print(f"Language: {locale.language}")
print(f"Country: {locale.country}")
# Display name: Japanese (Japan)
# Language: ja
# Country: JP
```

### Text Segmentation

Break text properly according to Unicode rules:

```python
# Grapheme segmentation (user-perceived characters)
text = "👨‍👩‍👧‍👦 family emoji"
graphemes = list(uicu.graphemes(text))
print(f"Graphemes: {graphemes}")
# Graphemes: ['👨‍👩‍👧‍👦', ' ', 'f', 'a', 'm', 'i', 'l', 'y', ' ', 'e', 'm', 'o', 'j', 'i']

# Word segmentation
words = list(uicu.words("Hello, world! 你好世界"))
print(f"Words: {[w.text for w in words if w.is_word]}")
# Words: ['Hello', 'world', '你好世界']
```

### Script Conversion

Transform text between writing systems:

```python
# Greek to Latin transliteration
greek_latin = uicu.Transliterator('Greek-Latin')
greek_text = "Ελληνικά"
latin_text = greek_latin.transliterate(greek_text)
print(f"{greek_text} → {latin_text}")
# Ελληνικά → Ellēniká

# Cyrillic to Latin
cyrillic_latin = uicu.Transliterator('Cyrillic-Latin')
russian_text = "Русский"
latin_text = cyrillic_latin.transliterate(russian_text)
print(f"{russian_text} → {latin_text}")
# Русский → Russkij
```

## Interactive Exploration

Try UICU's command-line interface for quick exploration:

```bash
# Analyze characters interactively
python -m uicu char "🚀"

# Compare collation rules
python -m uicu collate "café" "cafe" --locale en-US
python -m uicu collate "café" "cafe" --locale fr-FR

# Segment text
python -m uicu segment "Hello world! 你好" --type words
```

## Common Use Cases

### Input Validation

```python
def validate_username(username):
    for char in username:
        c = uicu.Char(char)
        if not (c.is_letter or c.is_digit or char in '_-'):
            return False, f"Invalid character: {char} ({c.name})"
    return True, "Valid username"

# Test usernames
print(validate_username("user_123"))  # (True, 'Valid username')
print(validate_username("user@123"))  # (False, 'Invalid character: @ (COMMERCIAL AT)')
```

### Text Normalization

```python
# Normalize text for comparison
def normalize_text(text):
    # Convert to NFC normalization
    normalized = uicu.normalize(text, 'NFC')
    # Case fold for case-insensitive comparison
    return uicu.case_fold(normalized)

text1 = "café"  # é as single character
text2 = "cafe\u0301"  # e + combining acute accent
print(f"Equal after normalization: {normalize_text(text1) == normalize_text(text2)}")
# Equal after normalization: True
```

### Language Detection

```python
# Basic script detection
def detect_script(text):
    scripts = {}
    for char in text:
        if uicu.Char(char).is_letter:
            script = uicu.Char(char).script
            scripts[script] = scripts.get(script, 0) + 1
    
    if scripts:
        return max(scripts, key=scripts.get)
    return 'Unknown'

print(detect_script("Hello"))      # Latin
print(detect_script("Привет"))     # Cyrillic  
print(detect_script("こんにちは"))  # Hiragana
```

## Next Steps

Now that you've seen UICU in action, explore these areas:

1. **[Installation](installation.md)** - Detailed setup for your platform
2. **[Unicode Basics](guide/unicode-basics.md)** - Understanding Unicode fundamentals
3. **[Character Properties](guide/character-properties.md)** - Deep dive into character analysis
4. **[API Reference](api/index.md)** - Complete API documentation

## Getting Help

- Check the [User Guide](guide/index.md) for comprehensive tutorials
- Browse [Examples](examples/index.md) for real-world use cases
- Report issues on [GitHub](https://github.com/twardoch/uicu/issues)

!!! tip "Performance Note"
    UICU caches expensive ICU objects automatically. Your first operation might be slower, but subsequent operations will be fast.

Ready to dive deeper? Let's explore [Unicode fundamentals](guide/unicode-basics.md) next!