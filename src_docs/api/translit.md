# uicu.translit

Text transformation and transliteration module.

This module provides powerful text transformation capabilities including script conversion, normalization, and custom transformations.

## Classes

### `Transliterator`

::: uicu.translit.Transliterator

## Functions

### `transliterate`

::: uicu.translit.transliterate

### `get_available_transforms`

::: uicu.translit.get_available_transforms

### `find_transforms`

::: uicu.translit.find_transforms

## Examples

### Basic Transliteration

```python
from uicu import Transliterator, transliterate

# Script conversion
greek_to_latin = Transliterator('Greek-Latin')
text = 'Ελληνικά'
result = greek_to_latin.transliterate(text)
print(f"{text} → {result}")  # 'Ellēniká'

# Quick transliteration
result = transliterate('Москва', 'Cyrillic-Latin')
print(result)  # 'Moskva'

# Case transformation
upper = Transliterator('Upper')
print(upper.transliterate('hello world'))  # 'HELLO WORLD'
```

### Script Conversion

```python
# Various script conversions
conversions = [
    ('Greek-Latin', 'Αθήνα'),
    ('Cyrillic-Latin', 'Москва'),
    ('Arabic-Latin', 'القاهرة'),
    ('Hebrew-Latin', 'ירושלים'),
    ('Thai-Latin', 'กรุงเทพ'),
    ('Devanagari-Latin', 'दिल्ली'),
    ('Han-Latin', '北京'),
    ('Hiragana-Latin', 'ひらがな'),
]

for transform, text in conversions:
    trans = Transliterator(transform)
    result = trans.transliterate(text)
    print(f"{transform:20} {text:15} → {result}")
```

### Accent and Diacritic Removal

```python
# Remove accents while preserving readability
deaccent = Transliterator('Latin-ASCII')

texts = [
    'café résumé',
    'naïve façade',
    'Zürich München',
    'señor niño',
    'Dvořák Janáček',
]

for text in texts:
    clean = deaccent.transliterate(text)
    print(f"'{text}' → '{clean}'")

# NFD decomposition + accent removal
nfd = Transliterator('NFD; [:M:] Remove; NFC')
print(nfd.transliterate('café'))  # 'cafe'
```

### Normalization

```python
# Unicode normalization forms
normalizers = {
    'NFC': Transliterator('NFC'),   # Canonical composition
    'NFD': Transliterator('NFD'),   # Canonical decomposition
    'NFKC': Transliterator('NFKC'), # Compatibility composition
    'NFKD': Transliterator('NFKD'), # Compatibility decomposition
}

# Test with various forms
test_strings = [
    'café',      # Precomposed é
    'café',      # Decomposed e + ́
    '㎡',        # Square meter symbol
    'ﬁ',         # fi ligature
    '①②③',      # Circled numbers
]

for text in test_strings:
    print(f"\nOriginal: '{text}' (length: {len(text)})")
    for name, trans in normalizers.items():
        result = trans.transliterate(text)
        print(f"  {name}: '{result}' (length: {len(result)})")
```

### Compound Transformations

```python
# Chain multiple transformations
compound = Transliterator('Greek-Latin; Latin-ASCII; Lower')
text = 'ΕΛΛΗΝΙΚΑ'
result = compound.transliterate(text)
print(f"{text} → {result}")  # 'ellenika'

# Complex transformation pipeline
pipeline = Transliterator('Any-Latin; Latin-ASCII; [:Punctuation:] Remove; Lower; NFC')
texts = [
    'Hello, World!',
    'Привет, мир!',
    '你好，世界！',
    'مرحبا بالعالم!',
]

for text in texts:
    result = pipeline.transliterate(text)
    print(f"'{text}' → '{result}'")
```

### Custom Transformations

```python
# Special transformations
special_transforms = [
    # Fullwidth/Halfwidth conversion
    ('Halfwidth-Fullwidth', 'Hello 123'),
    ('Fullwidth-Halfwidth', 'Ｈｅｌｌｏ　１２３'),
    
    # Hex encoding
    ('Any-Hex/Unicode', 'Hello 🌍'),
    ('Any-Hex/C', 'Test'),
    
    # Remove specific characters
    ('[:Punctuation:] Remove', 'Hello, World!'),
    ('[:WhiteSpace:] Remove', 'Hello World'),
    ('[:Digit:] Remove', 'Test123'),
]

for transform, text in special_transforms:
    trans = Transliterator(transform)
    result = trans.transliterate(text)
    print(f"{transform:30} '{text}' → '{result}'")
```

### Finding Available Transforms

```python
# Get all available transforms
all_transforms = get_available_transforms()
print(f"Total transforms available: {len(all_transforms)}")

# Find specific transforms
greek_transforms = find_transforms('Greek')
print(f"\nGreek-related transforms: {len(greek_transforms)}")
for t in sorted(greek_transforms)[:10]:
    print(f"  {t}")

# Find Latin transforms
latin_transforms = find_transforms('Latin')
print(f"\nLatin-related transforms: {len(latin_transforms)}")
for t in sorted(latin_transforms)[:10]:
    print(f"  {t}")
```

## Practical Applications

### URL Slug Generation

```python
def create_slug(text, max_length=50):
    """Convert text to URL-friendly slug."""
    # Transliterate to ASCII and clean
    trans = Transliterator('Any-Latin; Latin-ASCII; Lower')
    slug = trans.transliterate(text)
    
    # Replace non-alphanumeric with hyphens
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    
    # Truncate if needed
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]
    
    return slug

# Test with various inputs
titles = [
    "Hello World!",
    "Café René's Best Recipes",
    "Путеводитель по Москве",
    "東京オリンピック 2024",
    "🎉 Party Time! 🎊",
]

for title in titles:
    slug = create_slug(title)
    print(f"'{title}' → '{slug}'")
```

### Search Normalization

```python
class SearchNormalizer:
    """Normalize text for search operations."""
    
    def __init__(self):
        # Aggressive normalization for search
        self.normalizer = Transliterator(
            'NFD; [:M:] Remove; Latin-ASCII; Lower; '
            '[:Punctuation:] Remove; [:WhiteSpace:] > \' \'; NFC'
        )
    
    def normalize(self, text):
        """Normalize text for searching."""
        normalized = self.normalizer.transliterate(text)
        # Collapse multiple spaces
        return ' '.join(normalized.split())
    
    def match(self, text, query):
        """Check if normalized query matches normalized text."""
        return self.normalize(query) in self.normalize(text)

# Usage
normalizer = SearchNormalizer()

# Test data
products = [
    "Café René Premium",
    "Jose's Mexican Restaurant",
    "Zürich Swiss Chocolate",
    "naïve Art Gallery",
    "Dvořák Symphony Collection",
]

# Search queries
queries = ["cafe", "jose", "zurich", "naive", "dvorak"]

for query in queries:
    print(f"\nSearching for '{query}':")
    for product in products:
        if normalizer.match(product, query):
            print(f"  ✓ {product}")
```

### Data Cleaning

```python
class DataCleaner:
    """Clean and normalize data."""
    
    def __init__(self):
        self.transforms = {
            'normalize': Transliterator('NFC'),
            'ascii': Transliterator('Latin-ASCII'),
            'lower': Transliterator('Lower'),
            'no_punct': Transliterator('[:Punctuation:] Remove'),
            'no_space': Transliterator('[:WhiteSpace:] Remove'),
            'no_control': Transliterator('[:Control:] Remove'),
        }
    
    def clean_name(self, name):
        """Clean person name."""
        # Normalize and remove control characters
        name = self.transforms['normalize'].transliterate(name)
        name = self.transforms['no_control'].transliterate(name)
        return name.strip()
    
    def clean_email(self, email):
        """Clean email address."""
        # Lowercase and ASCII only
        email = self.transforms['lower'].transliterate(email)
        email = self.transforms['ascii'].transliterate(email)
        return email.strip()
    
    def clean_phone(self, phone):
        """Clean phone number."""
        # Remove everything except digits and +
        trans = Transliterator('[^0-9+] Remove')
        return trans.transliterate(phone)

# Example usage
cleaner = DataCleaner()

# Test data
test_data = [
    ("José García", "JOSÉ.GARCÍA@EXAMPLE.COM", "+1 (555) 123-4567"),
    ("François Müller", "françois@café.com", "555.867.5309"),
    ("李明", "li.ming@example.cn", "86-10-12345678"),
]

for name, email, phone in test_data:
    clean_name = cleaner.clean_name(name)
    clean_email = cleaner.clean_email(email)
    clean_phone = cleaner.clean_phone(phone)
    
    print(f"Original: {name}, {email}, {phone}")
    print(f"Cleaned:  {clean_name}, {clean_email}, {clean_phone}")
    print()
```

### Multi-Language Support

```python
def romanize_text(text):
    """Convert any script to Latin alphabet."""
    try:
        # Try to detect and convert
        trans = Transliterator('Any-Latin')
        return trans.transliterate(text)
    except Exception:
        # Fallback to basic ASCII
        trans = Transliterator('Latin-ASCII')
        return trans.transliterate(text)

# Test with various languages
multilingual = [
    ("English", "Hello World"),
    ("Russian", "Привет мир"),
    ("Greek", "Γεια σου κόσμε"),
    ("Arabic", "مرحبا بالعالم"),
    ("Chinese", "你好世界"),
    ("Japanese", "こんにちは世界"),
    ("Korean", "안녕하세요 세계"),
    ("Thai", "สวัสดีชาวโลก"),
    ("Hebrew", "שלום עולם"),
    ("Hindi", "नमस्ते दुनिया"),
]

for lang, text in multilingual:
    romanized = romanize_text(text)
    print(f"{lang:10} {text:20} → {romanized}")
```

## Performance Tips

1. **Reuse Transliterators**: Creating transliterators is expensive. Create once and reuse.

2. **Batch Processing**: Process multiple strings with the same transliterator.

3. **Choose Appropriate Transforms**: Some transforms are more expensive than others.

```python
import time

# Performance comparison
text = "Ελληνικά " * 1000
transform = 'Greek-Latin'

# Method 1: Create new transliterator each time (slow)
start = time.time()
for _ in range(100):
    trans = Transliterator(transform)
    result = trans.transliterate(text)
slow_time = time.time() - start

# Method 2: Reuse transliterator (fast)
trans = Transliterator(transform)
start = time.time()
for _ in range(100):
    result = trans.transliterate(text)
fast_time = time.time() - start

print(f"Create each time: {slow_time:.3f}s")
print(f"Reuse: {fast_time:.3f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

## Common Patterns

### Safe Transliteration

```python
def safe_transliterate(text, transform):
    """Safely transliterate with error handling."""
    try:
        trans = Transliterator(transform)
        return trans.transliterate(text)
    except Exception as e:
        print(f"Warning: Failed to apply {transform}: {e}")
        return text  # Return original on error

# Test with potentially problematic transforms
test_cases = [
    ('Valid transform', 'Hello', 'Upper'),
    ('Invalid transform', 'Hello', 'InvalidTransform'),
    ('Empty text', '', 'Lower'),
]

for name, text, transform in test_cases:
    result = safe_transliterate(text, transform)
    print(f"{name}: '{text}' → '{result}'")
```

### Transform Validation

```python
def is_valid_transform(transform_id):
    """Check if a transform ID is valid."""
    try:
        Transliterator(transform_id)
        return True
    except Exception:
        return False

# Test various transform IDs
transforms = [
    'Upper',
    'Lower',
    'Greek-Latin',
    'Invalid-Transform',
    'NFC',
    'Any-Latin; Latin-ASCII',
]

for t in transforms:
    valid = is_valid_transform(t)
    print(f"{t:30} {'✓' if valid else '✗'}")
```

## See Also

- [Transliteration Guide](../guide/transliteration.md) - Detailed usage guide
- [Script Conversion Examples](../examples/script-conversion.md) - More examples
- [`uicu.char`](char.md) - Character script information