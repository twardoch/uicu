# Getting Started with UICU

This guide will help you get up and running with UICU in just a few minutes.

## Prerequisites

Before installing UICU, ensure you have:

- **Python 3.10 or later**
- **pip** or **uv** package manager
- **C++ compiler** (for building PyICU if needed)

## Quick Installation

=== "pip"

    ```bash
    pip install uicu
    ```

=== "uv"

    ```bash
    uv pip install uicu
    ```

=== "From Source"

    ```bash
    git clone https://github.com/twardoch/uicu.git
    cd uicu
    pip install -e .
    ```

## First Steps

### 1. Import UICU

```python
import uicu

# Check the version
print(f"UICU version: {uicu.__version__}")
```

### 2. Explore Unicode Characters

```python
# Create a character object
char = uicu.Char('🎉')

# Get character properties
print(f"Character: {char.value}")
print(f"Name: {char.name}")
print(f"Category: {char.category}")
print(f"Script: {char.script}")
print(f"Block: {char.block}")
```

### 3. Work with Locales

```python
# Get your system's default locale
default_locale = uicu.get_default_locale()
print(f"Default locale: {default_locale.language_tag}")

# Create a specific locale
locale = uicu.Locale('fr-FR')
print(f"Display name: {locale.display_name}")
print(f"Language: {locale.language}")
print(f"Region: {locale.region}")
```

### 4. Sort Text Properly

```python
# Create a locale-aware collator
collator = uicu.Collator('en-US')

# Sort a list of names
names = ['André', 'Andrew', 'andrea', 'Ándrea']
sorted_names = collator.sort(names)
print(f"Sorted: {sorted_names}")

# Use numeric sorting
numeric_collator = uicu.Collator('en-US', numeric=True)
items = ['item10', 'item2', 'item1', 'item20']
print(f"Numeric sort: {numeric_collator.sort(items)}")
```

### 5. Segment Text

```python
# Break text into words
text = "Hello, world! How are you?"
words = list(uicu.words(text))
print(f"Words: {words}")

# Handle complex scripts
thai_text = "สวัสดีครับ ยินดีต้อนรับ"
thai_words = list(uicu.words(thai_text, locale='th-TH'))
print(f"Thai words: {thai_words}")

# Work with grapheme clusters
emoji_text = "👨‍👩‍👧‍👦👋🏾🇺🇸"
graphemes = list(uicu.graphemes(emoji_text))
print(f"Graphemes: {graphemes}")
```

### 6. Transform Text

```python
# Transliterate between scripts
greek = uicu.Transliterator('Greek-Latin')
print(greek.transliterate('Ελληνικά'))  # 'Ellēniká'

# Remove accents
deaccent = uicu.Transliterator('Latin-ASCII')
print(deaccent.transliterate('café résumé naïve'))  # 'cafe resume naive'

# Convert to uppercase
upper = uicu.Transliterator('Upper')
print(upper.transliterate('hello world'))  # 'HELLO WORLD'
```

## Complete Example

Here's a complete example that demonstrates multiple UICU features:

```python
import uicu
from datetime import datetime

def analyze_text(text: str, locale_id: str = 'en-US'):
    """Analyze text using various UICU features."""
    print(f"\nAnalyzing: '{text}'")
    print(f"Locale: {locale_id}")
    print("-" * 50)
    
    # Create locale
    locale = uicu.Locale(locale_id)
    print(f"Locale display name: {locale.display_name}")
    
    # Character analysis
    print("\nCharacter Analysis:")
    for i, char in enumerate(text[:5]):  # First 5 chars
        if not char.isspace():
            c = uicu.Char(char)
            print(f"  '{char}': {c.name} ({c.category})")
    
    # Text segmentation
    print("\nText Segmentation:")
    words = list(uicu.words(text, locale=locale_id))
    print(f"  Words ({len(words)}): {words[:10]}...")  # First 10 words
    
    sentences = list(uicu.sentences(text, locale=locale_id))
    print(f"  Sentences ({len(sentences)}): {sentences[0][:50]}...")
    
    # Script detection
    script = uicu.detect_script(text)
    if script:
        print(f"\nPrimary script: {script}")
    
    # Collation
    if len(words) > 1:
        collator = uicu.Collator(locale_id)
        sorted_words = collator.sort(words)[:5]  # First 5 sorted
        print(f"\nFirst 5 sorted words: {sorted_words}")

# Test with different texts
analyze_text("Hello, world! How are you doing today?")
analyze_text("Bonjour le monde! Comment allez-vous?", "fr-FR")
analyze_text("你好世界！今天过得怎么样？", "zh-CN")
```

## Common Patterns

### Error Handling

```python
try:
    # Try to create a character from invalid input
    char = uicu.Char('ab')  # Multi-character string
except uicu.UICUError as e:
    print(f"Error: {e}")

# Use the functional API for safety
name = uicu.name('🎉')  # Always returns a string or None
```

### Performance Tips

```python
# Reuse expensive objects
collator = uicu.Collator('en-US')  # Create once
for dataset in datasets:
    sorted_data = collator.sort(dataset)  # Use many times

# Use locale objects for multiple operations
locale = uicu.Locale('de-DE')
collator = locale.get_collator()
formatter = locale.get_datetime_formatter()
```

### Working with Unknown Text

```python
def process_unknown_text(text: str):
    """Safely process text of unknown origin."""
    # Detect script
    script = uicu.detect_script(text)
    
    # Choose appropriate locale
    locale_map = {
        'Hani': 'zh-CN',  # Chinese
        'Jpan': 'ja-JP',  # Japanese
        'Arab': 'ar-SA',  # Arabic
        'Cyrl': 'ru-RU',  # Cyrillic
        'Thai': 'th-TH',  # Thai
    }
    locale_id = locale_map.get(script, 'en-US')
    
    # Process with detected locale
    words = list(uicu.words(text, locale=locale_id))
    return words
```

## What's Next?

Now that you've seen the basics, explore more advanced features:

- **[Unicode Basics](guide/unicode-basics.md)** - Understanding Unicode concepts
- **[Character Properties](guide/character-properties.md)** - Deep dive into character analysis
- **[Text Collation](guide/text-collation.md)** - Advanced sorting techniques
- **[Examples](examples/index.md)** - Real-world usage examples

## Need Help?

- Check the [API Reference](api/index.md) for detailed documentation
- Browse [Examples](examples/index.md) for common use cases
- Report issues on [GitHub](https://github.com/twardoch/uicu/issues)