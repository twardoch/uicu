# Transliteration

Transliteration is the process of converting text from one script to another or applying text transformations. UICU provides powerful transliteration capabilities through ICU's transform engine.

## Understanding Transliteration

Transliteration serves many purposes:
- **Script conversion**: Greek → Latin, Cyrillic → Latin
- **Normalization**: Removing accents, case conversion
- **Text cleanup**: Standardizing variations
- **Phonetic representation**: Converting to pronunciation

```python
import uicu

# Quick examples
greek = uicu.Transliterator('Greek-Latin')
print(greek.transliterate('Ελληνικά'))  # 'Ellēniká'

deaccent = uicu.Transliterator('Latin-ASCII')
print(deaccent.transliterate('café résumé'))  # 'cafe resume'

upper = uicu.Transliterator('Upper')
print(upper.transliterate('hello world'))  # 'HELLO WORLD'
```

## Basic Transliteration

### Creating Transliterators

```python
# Different ways to create transliterators
trans1 = uicu.Transliterator('Latin-ASCII')  # Direct creation
trans2 = uicu.Transliterator.create_instance('Upper')  # Factory method

# Compound transforms
trans3 = uicu.Transliterator('Greek-Latin; Latin-ASCII; Lower')

# From locale
locale = uicu.Locale('el-GR')  # Greek
# Locale-specific transliterators can be created if needed
```

### Common Transformations

```python
# Case transformations
upper = uicu.Transliterator('Upper')
lower = uicu.Transliterator('Lower')
title = uicu.Transliterator('Title')

text = "hello WORLD Example"
print(f"Upper: {upper.transliterate(text)}")
print(f"Lower: {lower.transliterate(text)}")
print(f"Title: {title.transliterate(text)}")

# Normalization
nfc = uicu.Transliterator('NFC')  # Canonical composition
nfd = uicu.Transliterator('NFD')  # Canonical decomposition

text = "café"  # Could be é or e+́
print(f"NFC: {nfc.transliterate(text)}")
print(f"NFD: {nfd.transliterate(text)}")
print(f"NFD length: {len(nfd.transliterate(text))}")  # More code points
```

## Script-to-Script Conversion

### Basic Script Conversion

```python
# Create script converters
converters = {
    'Greek-Latin': uicu.Transliterator('Greek-Latin'),
    'Cyrillic-Latin': uicu.Transliterator('Cyrillic-Latin'),
    'Arabic-Latin': uicu.Transliterator('Arabic-Latin'),
    'Hebrew-Latin': uicu.Transliterator('Hebrew-Latin'),
    'Thai-Latin': uicu.Transliterator('Thai-Latin'),
    'Devanagari-Latin': uicu.Transliterator('Devanagari-Latin'),
}

# Test conversions
test_texts = {
    'Greek-Latin': 'Ελληνική Δημοκρατία',
    'Cyrillic-Latin': 'Россия Москва',
    'Arabic-Latin': 'مرحبا بالعالم',
    'Hebrew-Latin': 'שלום עולם',
    'Thai-Latin': 'สวัสดีครับ',
    'Devanagari-Latin': 'नमस्ते भारत',
}

for transform, text in test_texts.items():
    if transform in converters:
        result = converters[transform].transliterate(text)
        print(f"{transform:20} '{text}' → '{result}'")
```

### Reversible Transliteration

```python
# Some transforms are reversible
latin_to_greek = uicu.Transliterator('Latin-Greek')
greek_to_latin = uicu.Transliterator('Greek-Latin')

original = "Athena"
to_greek = latin_to_greek.transliterate(original)
back_to_latin = greek_to_latin.transliterate(to_greek)

print(f"Original: {original}")
print(f"To Greek: {to_greek}")
print(f"Back to Latin: {back_to_latin}")

# Note: Not always perfect due to ambiguities
```

### Script Variants

```python
# Different romanization systems
chinese_pinyin = uicu.Transliterator('Han-Latin')
japanese_romaji = uicu.Transliterator('Hiragana-Latin')
korean_romanize = uicu.Transliterator('Hangul-Latin')

examples = [
    ('Chinese', '北京', chinese_pinyin),
    ('Japanese', 'ひらがな', japanese_romaji),
    ('Korean', '한글', korean_romanize),
]

for script, text, trans in examples:
    result = trans.transliterate(text)
    print(f"{script}: '{text}' → '{result}'")
```

## Accent and Diacritic Removal

### Basic Accent Removal

```python
# Remove accents while preserving base letters
deaccent = uicu.Transliterator('Latin-ASCII')

accented_texts = [
    'café résumé',
    'naïve façade',
    'Zürich München',
    'señor niño',
    'garçon français',
    'Dvořák Janáček',
]

for text in accented_texts:
    clean = deaccent.transliterate(text)
    print(f"'{text}' → '{clean}'")
```

### Preserving Special Characters

```python
# NFD + remove combining marks
def remove_accents_preserve_special(text):
    # Decompose
    nfd = uicu.Transliterator('NFD')
    decomposed = nfd.transliterate(text)
    
    # Remove combining marks manually
    result = ""
    for char in decomposed:
        if uicu.category(char) not in ('Mn', 'Mc', 'Me'):  # Not a mark
            result += char
    
    return result

# Test with special characters
texts = [
    'café €100',  # Euro sign should be preserved
    'résumé™',    # Trademark should be preserved
    'naïve ©2024', # Copyright should be preserved
]

deaccent = uicu.Transliterator('Latin-ASCII')
for text in texts:
    # Standard Latin-ASCII
    standard = deaccent.transliterate(text)
    # Custom preservation
    custom = remove_accents_preserve_special(text)
    print(f"Original: '{text}'")
    print(f"  Standard: '{standard}'")
    print(f"  Custom: '{custom}'")
```

## Compound Transformations

### Chaining Transforms

```python
# Apply multiple transformations in sequence
chain = uicu.Transliterator('Greek-Latin; Latin-ASCII; Lower')

greek_text = "ΕΛΛΗΝΙΚΑ"
result = chain.transliterate(greek_text)
print(f"'{greek_text}' → '{result}'")

# Step by step
trans1 = uicu.Transliterator('Greek-Latin')
trans2 = uicu.Transliterator('Latin-ASCII')
trans3 = uicu.Transliterator('Lower')

text = greek_text
print(f"Original: {text}")
text = trans1.transliterate(text)
print(f"After Greek-Latin: {text}")
text = trans2.transliterate(text)
print(f"After Latin-ASCII: {text}")
text = trans3.transliterate(text)
print(f"After Lower: {text}")
```

### Complex Transform Chains

```python
# Normalize and clean text
def create_url_slug(text):
    """Convert text to URL-friendly slug."""
    # Chain: Any script to Latin, remove accents, lowercase
    trans = uicu.Transliterator('Any-Latin; Latin-ASCII; Lower')
    
    # Apply transformations
    slug = trans.transliterate(text)
    
    # Replace spaces and special chars with hyphens
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    
    return slug

# Test with various inputs
titles = [
    "Hello World!",
    "Café René",
    "北京 2024",
    "Москва-Сити",
    "🎉 Party Time!!!",
    "C++ Programming",
]

for title in titles:
    slug = create_url_slug(title)
    print(f"'{title}' → '{slug}'")
```

## Special Transformations

### Fullwidth/Halfwidth Conversion

```python
# Convert between fullwidth and halfwidth characters
fullwidth = uicu.Transliterator('Halfwidth-Fullwidth')
halfwidth = uicu.Transliterator('Fullwidth-Halfwidth')

# Halfwidth (normal) text
normal = "Hello 123 ABC"
fw = fullwidth.transliterate(normal)
print(f"Normal: '{normal}'")
print(f"Fullwidth: '{fw}'")

# Convert back
hw = halfwidth.transliterate(fw)
print(f"Back to halfwidth: '{hw}'")

# Common in Japanese text
japanese_mixed = "ｶﾀｶﾅ　カタカナ　123　１２３"
normalized = halfwidth.transliterate(japanese_mixed)
print(f"Japanese mixed: '{japanese_mixed}'")
print(f"Normalized: '{normalized}'")
```

### Hex and Name Transforms

```python
# Convert to hex representation
hex_trans = uicu.Transliterator('Any-Hex/Unicode')
text = "Hello 世界 🌍"
hex_text = hex_trans.transliterate(text)
print(f"Text: '{text}'")
print(f"Hex: '{hex_text}'")

# Convert hex back to text
hex_to_text = uicu.Transliterator('Hex/Unicode-Any')
restored = hex_to_text.transliterate(hex_text)
print(f"Restored: '{restored}'")

# Character names (if available in ICU build)
try:
    name_trans = uicu.Transliterator('Any-Name')
    char = "€"
    name = name_trans.transliterate(char)
    print(f"Character '{char}' name: {name}")
except:
    print("Name transform not available")
```

## Practical Examples

### Text Normalization Pipeline

```python
class TextNormalizer:
    """Comprehensive text normalization."""
    
    def __init__(self):
        # Create transliterators
        self.to_nfc = uicu.Transliterator('NFC')
        self.to_latin = uicu.Transliterator('Any-Latin')
        self.to_ascii = uicu.Transliterator('Latin-ASCII')
        self.to_lower = uicu.Transliterator('Lower')
        self.strip_marks = uicu.Transliterator('[:M:] Remove')
    
    def normalize(self, text, level='full'):
        """Normalize text at specified level."""
        if level == 'minimal':
            # Just NFC normalization
            return self.to_nfc.transliterate(text)
        
        elif level == 'moderate':
            # NFC + lowercase
            text = self.to_nfc.transliterate(text)
            text = self.to_lower.transliterate(text)
            return text
        
        elif level == 'full':
            # Full normalization pipeline
            text = self.to_nfc.transliterate(text)
            text = self.to_latin.transliterate(text)
            text = self.to_ascii.transliterate(text)
            text = self.to_lower.transliterate(text)
            return text
        
        else:
            raise ValueError(f"Unknown level: {level}")
    
    def normalize_for_search(self, text):
        """Normalize for search indexing."""
        # Remove all marks and normalize
        text = self.to_nfc.transliterate(text)
        text = self.to_lower.transliterate(text)
        text = self.strip_marks.transliterate(text)
        return text

# Example usage
normalizer = TextNormalizer()

test_texts = [
    "Café RÉSUMÉ",
    "Москва 2024",
    "東京タワー",
    "naïve façade",
]

print("Normalization levels:")
for text in test_texts:
    print(f"\nOriginal: '{text}'")
    print(f"  Minimal: '{normalizer.normalize(text, 'minimal')}'")
    print(f"  Moderate: '{normalizer.normalize(text, 'moderate')}'")
    print(f"  Full: '{normalizer.normalize(text, 'full')}'")
    print(f"  Search: '{normalizer.normalize_for_search(text)}'")
```

### Multi-Script Document Processing

```python
def process_multilingual_document(text):
    """Process document with mixed scripts."""
    # Detect primary script
    primary_script = uicu.detect_script(text)
    print(f"Primary script: {primary_script}")
    
    # Create appropriate transliterator
    if primary_script == 'Cyrl':
        trans = uicu.Transliterator('Cyrillic-Latin')
    elif primary_script == 'Grek':
        trans = uicu.Transliterator('Greek-Latin')
    elif primary_script == 'Arab':
        trans = uicu.Transliterator('Arabic-Latin')
    else:
        trans = uicu.Transliterator('Any-Latin')
    
    # Process text
    romanized = trans.transliterate(text)
    
    # Clean up
    clean = uicu.Transliterator('Latin-ASCII; Lower')
    cleaned = clean.transliterate(romanized)
    
    return {
        'original': text,
        'romanized': romanized,
        'cleaned': cleaned,
        'script': primary_script
    }

# Test documents
documents = [
    "Добро пожаловать в Москву!",
    "Καλώς ήρθατε στην Αθήνα!",
    "Welcome to London!",
    "مرحبا بكم في دبي!",
]

for doc in documents:
    result = process_multilingual_document(doc)
    print(f"\nDocument processing:")
    print(f"  Original: {result['original']}")
    print(f"  Script: {result['script']}")
    print(f"  Romanized: {result['romanized']}")
    print(f"  Cleaned: {result['cleaned']}")
```

### Search Term Normalization

```python
class SearchNormalizer:
    """Normalize search terms for matching."""
    
    def __init__(self):
        # Create transform chain for aggressive normalization
        transforms = [
            'NFD',           # Decompose
            '[:M:] Remove',  # Remove marks
            'Latin-ASCII',   # Remove remaining accents
            'Lower',         # Lowercase
            'NFC',          # Recompose
        ]
        self.normalizer = uicu.Transliterator('; '.join(transforms))
    
    def normalize(self, text):
        """Aggressively normalize for search."""
        # Apply transforms
        normalized = self.normalizer.transliterate(text)
        
        # Additional cleanup
        import re
        # Remove punctuation
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        # Collapse whitespace
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def match(self, text, query):
        """Check if query matches text (normalized)."""
        norm_text = self.normalize(text)
        norm_query = self.normalize(query)
        return norm_query in norm_text

# Example usage
searcher = SearchNormalizer()

# Test data
items = [
    "Café René",
    "Jose's Restaurant",
    "Zürich Hotel",
    "naïve art gallery",
    "Dvořák Symphony",
]

# Search queries
queries = [
    "cafe",
    "jose",
    "zurich",
    "naive",
    "dvorak",
]

print("Search matching:")
for query in queries:
    print(f"\nSearching for '{query}':")
    matches = [item for item in items if searcher.match(item, query)]
    for match in matches:
        print(f"  ✓ {match}")
```

## Available Transforms

### Finding Available Transforms

```python
# Get list of available transforms
available = uicu.get_available_transforms()
print(f"Total available transforms: {len(available)}")

# Show some categories
script_to_latin = [t for t in available if t.endswith('-Latin')]
print(f"\nScript-to-Latin transforms: {len(script_to_latin)}")
for transform in sorted(script_to_latin)[:10]:
    print(f"  {transform}")

# Case transforms
case_transforms = [t for t in available if any(x in t for x in ['Upper', 'Lower', 'Title'])]
print(f"\nCase transforms:")
for transform in sorted(case_transforms):
    print(f"  {transform}")
```

### Searching for Transforms

```python
# Find transforms for specific needs
def find_transforms_for(script_or_name):
    """Find transforms related to a script or name."""
    available = uicu.get_available_transforms()
    matches = []
    
    search = script_or_name.lower()
    for transform in available:
        if search in transform.lower():
            matches.append(transform)
    
    return sorted(matches)

# Examples
print("Greek-related transforms:")
for t in find_transforms_for('Greek')[:5]:
    print(f"  {t}")

print("\nArabic-related transforms:")
for t in find_transforms_for('Arabic')[:5]:
    print(f"  {t}")

print("\nAccent-related transforms:")
for t in find_transforms_for('ASCII')[:5]:
    print(f"  {t}")
```

## Performance Tips

### Reuse Transliterators

```python
import time

text = "Ελληνικά " * 1000

# Bad: Create new transliterator each time
start = time.time()
for _ in range(100):
    trans = uicu.Transliterator('Greek-Latin')
    result = trans.transliterate(text)
slow_time = time.time() - start

# Good: Reuse transliterator
trans = uicu.Transliterator('Greek-Latin')
start = time.time()
for _ in range(100):
    result = trans.transliterate(text)
fast_time = time.time() - start

print(f"Create each time: {slow_time:.3f}s")
print(f"Reuse: {fast_time:.3f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

### Batch Processing

```python
def batch_transliterate(texts, transform_id):
    """Efficiently transliterate multiple texts."""
    trans = uicu.Transliterator(transform_id)
    return [trans.transliterate(text) for text in texts]

# Example
greek_texts = ['Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Ηράκλειο'] * 100
romanized = batch_transliterate(greek_texts, 'Greek-Latin')
print(f"Processed {len(romanized)} texts")
```

## Common Use Cases

### 1. URL Slug Generation

```python
def make_url_slug(title, max_length=50):
    """Convert title to URL-friendly slug."""
    # Transliterate to ASCII
    trans = uicu.Transliterator('Any-Latin; Latin-ASCII; Lower')
    slug = trans.transliterate(title)
    
    # Replace non-alphanumeric with hyphens
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    
    # Truncate if needed
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]
    
    return slug

titles = [
    "10 Tips for Café Owners",
    "Путешествие в Москву",
    "東京オリンピック2024",
    "C++ vs. Java: Which is Better?",
]

for title in titles:
    slug = make_url_slug(title)
    print(f"'{title}'")
    print(f"  → {slug}")
```

### 2. Search Indexing

```python
def prepare_for_indexing(text):
    """Prepare text for search indexing."""
    # Normalize aggressively
    transforms = [
        'Any-Latin',      # Convert to Latin
        'Latin-ASCII',    # Remove accents
        'Lower',          # Lowercase
        '[:P:] Remove',   # Remove punctuation
    ]
    
    trans = uicu.Transliterator('; '.join(transforms))
    indexed = trans.transliterate(text)
    
    # Clean up whitespace
    indexed = ' '.join(indexed.split())
    
    return indexed

# Example
documents = [
    "Café René's Best Recipes!",
    "Москва: Путеводитель 2024",
    "C++ Programming (Advanced)",
    "naïve Bayes classifier",
]

for doc in documents:
    indexed = prepare_for_indexing(doc)
    print(f"Original: '{doc}'")
    print(f"Indexed: '{indexed}'")
    print()
```

### 3. Data Cleaning

```python
def clean_user_input(text):
    """Clean and normalize user input."""
    # Remove invisible characters and normalize
    trans = uicu.Transliterator('NFC; [:Cf:] Remove; [:Cc:] Remove')
    
    cleaned = trans.transliterate(text)
    cleaned = cleaned.strip()
    
    return cleaned

# Test with problematic input
inputs = [
    "Hello\u200B World",  # Zero-width space
    "Test\u0000ing",      # Null character
    "Café\u00AD",         # Soft hyphen
    "Normal text",
]

for text in inputs:
    cleaned = clean_user_input(text)
    print(f"Original: {text!r}")
    print(f"Cleaned: {cleaned!r}")
    print()
```

## Next Steps

- Explore [Date/Time Formatting](date-time-formatting.md) for locale-specific display
- Review [Best Practices](best-practices.md) for text processing
- See [Examples](../examples/script-conversion.md) for more use cases