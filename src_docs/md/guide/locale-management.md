---
# this_file: src_docs/md/guide/locale-management.md
title: Locale Management
description: Internationalization with 700+ locales
---

# Locale Management

UICU provides comprehensive locale support for internationalization, handling cultural and regional variations in text processing across 700+ locales.

## Understanding Locales

A locale defines cultural and linguistic conventions for a specific region:

```python
import uicu

# Create locale instances
us_english = uicu.Locale('en-US')
uk_english = uicu.Locale('en-GB') 
french = uicu.Locale('fr-FR')
japanese = uicu.Locale('ja-JP')
arabic = uicu.Locale('ar-SA')

print(f"US English: {us_english.display_name}")
print(f"UK English: {uk_english.display_name}")
print(f"French: {french.display_name}")
print(f"Japanese: {japanese.display_name}")
print(f"Arabic: {arabic.display_name}")
```

## Locale Components

### Language, Script, Region, and Variants

```python
# Analyze locale components
locales = [
    'en-US',           # English, United States
    'zh-Hans-CN',      # Chinese, Simplified script, China
    'sr-Cyrl-RS',      # Serbian, Cyrillic script, Serbia
    'de-DE-1996',      # German, Germany, 1996 spelling reform
    'ca-ES-valencia',  # Catalan, Spain, Valencian variant
]

for locale_id in locales:
    locale = uicu.Locale(locale_id)
    print(f"\nLocale: {locale_id}")
    print(f"  Language: {locale.language} ({locale.language_display_name})")
    print(f"  Script: {locale.script} ({locale.script_display_name})")
    print(f"  Country: {locale.country} ({locale.country_display_name})")
    print(f"  Variant: {locale.variant} ({locale.variant_display_name})")
    print(f"  Display name: {locale.display_name}")
```

### Available Locales

```python
# List available locales
all_locales = uicu.Locale.get_available_locales()
print(f"Total available locales: {len(all_locales)}")

# Filter by language
english_locales = [loc for loc in all_locales if loc.language == 'en']
print(f"English locales: {len(english_locales)}")

# Display first few English locales
for locale in english_locales[:10]:
    print(f"  {locale.id}: {locale.display_name}")
```

## Locale-Specific Text Processing

### Case Conversion

Different languages have different case rules:

```python
# Turkish I problem
text = "İstanbul"

turkish_locale = uicu.Locale('tr-TR')
english_locale = uicu.Locale('en-US')

turkish_lower = uicu.lower(text, locale=turkish_locale)
english_lower = uicu.lower(text, locale=english_locale)

print(f"Original: {text}")
print(f"Turkish lowercase: {turkish_lower}")  # istanbul (dotless i)
print(f"English lowercase: {english_lower}")  # i̇stanbul (dotted i)

# German sharp s
german_text = "Straße"
german_locale = uicu.Locale('de-DE')

print(f"\nGerman text: {german_text}")
print(f"German uppercase: {uicu.upper(german_text, locale=german_locale)}")  # STRASSE
```

### Collation (Sorting)

Locale-aware text sorting follows cultural conventions:

```python
# German collation - treats ä as 'ae'
german_words = ['Müller', 'Mueller', 'Mahler', 'Möller']

# Default (Unicode) sorting
default_sorted = sorted(german_words)
print(f"Default sort: {default_sorted}")

# German locale sorting
german_collator = uicu.Collator('de-DE')
german_sorted = german_collator.sort(german_words)
print(f"German sort: {german_sorted}")

# French collation - ignores accents in primary comparison
french_words = ['côte', 'coté', 'cote', 'côté']
french_collator = uicu.Collator('fr-FR')
french_sorted = french_collator.sort(french_words)
print(f"French sort: {french_sorted}")
```

### Number Formatting

Numbers are formatted differently across locales:

```python
# Different number formatting conventions
number = 1234567.89

locales_to_test = ['en-US', 'de-DE', 'fr-FR', 'hi-IN', 'ar-SA']

for locale_id in locales_to_test:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_number_formatter()
    formatted = formatter.format(number)
    print(f"{locale.display_name:20}: {formatted}")
```

### Date and Time Formatting

Date and time representation varies significantly:

```python
from datetime import datetime

# Current date/time
now = datetime.now()

# Different locale formatting
datetime_locales = [
    ('en-US', 'US English'),
    ('en-GB', 'UK English'), 
    ('de-DE', 'German'),
    ('ja-JP', 'Japanese'),
    ('ar-SA', 'Arabic'),
]

for locale_id, name in datetime_locales:
    locale = uicu.Locale(locale_id)
    
    # Date formatter
    date_formatter = locale.get_date_formatter(style='medium')
    formatted_date = date_formatter.format(now)
    
    # Time formatter
    time_formatter = locale.get_time_formatter(style='short')
    formatted_time = time_formatter.format(now)
    
    print(f"{name:12}: {formatted_date} {formatted_time}")
```

## Locale Discovery and Fallback

### Locale Negotiation

```python
def negotiate_locale(requested_locales, available_locales):
    """Find best matching locale from available options"""
    for requested in requested_locales:
        # Try exact match first
        if requested in available_locales:
            return requested
        
        # Try language match
        req_lang = uicu.Locale(requested).language
        for available in available_locales:
            if uicu.Locale(available).language == req_lang:
                return available
    
    # Fallback to default
    return 'en-US'

# Example negotiation
user_preferences = ['fr-CA', 'fr-FR', 'en-CA', 'en-US']
app_locales = ['en-US', 'fr-FR', 'de-DE', 'ja-JP']

best_locale = negotiate_locale(user_preferences, app_locales)
print(f"User preferences: {user_preferences}")
print(f"Available locales: {app_locales}")
print(f"Selected locale: {best_locale}")
```

### Locale Fallback Chain

```python
def get_fallback_chain(locale_id):
    """Get locale fallback chain"""
    locale = uicu.Locale(locale_id)
    chain = [locale.id]
    
    # Add parent locales
    current = locale
    while current.parent:
        current = current.parent
        chain.append(current.id)
    
    # Add root
    if chain[-1] != 'root':
        chain.append('root')
    
    return chain

# Example fallback chains
test_locales = ['zh-Hans-CN', 'en-GB', 'pt-BR']
for locale_id in test_locales:
    chain = get_fallback_chain(locale_id)
    print(f"{locale_id}: {' → '.join(chain)}")
```

## Text Direction and Layout

### Bidirectional Text Support

```python
# Mixed LTR/RTL text
mixed_texts = [
    "Hello שלום World",                    # English-Hebrew-English
    "مرحبا Hello عالم",                    # Arabic-English-Arabic
    "Price: $100 السعر: ١٠٠ ريال",         # Mixed numbers and currencies
]

for text in mixed_texts:
    # Analyze text direction
    direction = uicu.get_base_direction(text)
    print(f"Text: {text}")
    print(f"Base direction: {direction}")
    
    # Get directional runs
    runs = uicu.get_bidi_runs(text)
    for run in runs:
        print(f"  '{run.text}' ({run.direction})")
    print()
```

### Writing System Properties

```python
def analyze_writing_system(locale_id):
    """Analyze writing system properties of a locale"""
    locale = uicu.Locale(locale_id)
    
    # Get exemplar characters (typical characters used)
    exemplars = locale.get_exemplar_set()
    
    # Get likely script
    likely_script = locale.get_likely_script()
    
    # Check if RTL
    is_rtl = locale.is_rtl()
    
    return {
        'locale': locale.display_name,
        'script': likely_script,
        'rtl': is_rtl,
        'exemplars': exemplars[:20] if exemplars else None,  # First 20 chars
    }

# Analyze different writing systems
writing_systems = ['en-US', 'ar-SA', 'zh-CN', 'ja-JP', 'he-IL', 'th-TH']
for locale_id in writing_systems:
    info = analyze_writing_system(locale_id)
    print(f"{info['locale']}:")
    print(f"  Script: {info['script']}")
    print(f"  RTL: {info['rtl']}")
    print(f"  Sample chars: {info['exemplars']}")
    print()
```

## Currency and Numeric Conventions

### Currency Formatting

```python
# Currency formatting varies by locale
amount = 1234.56

currency_examples = [
    ('en-US', 'USD'),  # $1,234.56
    ('de-DE', 'EUR'),  # 1.234,56 €
    ('ja-JP', 'JPY'),  # ¥1,235 (no decimals)
    ('ar-SA', 'SAR'),  # ١٬٢٣٤٫٥٦ ر.س.
    ('hi-IN', 'INR'),  # ₹1,234.56
]

for locale_id, currency_code in currency_examples:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_currency_formatter(currency_code)
    formatted = formatter.format(amount)
    print(f"{locale.display_name:15}: {formatted}")
```

### Number Systems

```python
# Different number systems
number = 12345

number_systems = [
    ('en-US', 'Western digits'),
    ('ar-SA', 'Arabic-Indic digits'),
    ('hi-IN', 'Devanagari digits'),
    ('th-TH', 'Thai digits'),
    ('my-MM', 'Myanmar digits'),
]

for locale_id, description in number_systems:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_number_formatter()
    formatted = formatter.format(number)
    print(f"{description:20}: {formatted}")
```

## Practical Applications

### User Interface Localization

```python
class LocalizedUI:
    """Simple localized user interface"""
    
    def __init__(self, locale_id):
        self.locale = uicu.Locale(locale_id)
        self.collator = uicu.Collator(locale_id)
        self.date_formatter = self.locale.get_date_formatter(style='medium')
        self.number_formatter = self.locale.get_number_formatter()
    
    def format_user_count(self, count):
        """Format user count with proper pluralization"""
        formatted_number = self.number_formatter.format(count)
        
        # Simple pluralization (real apps would use ICU MessageFormat)
        if self.locale.language == 'en':
            plural = 'user' if count == 1 else 'users'
        elif self.locale.language == 'de':
            plural = 'Benutzer'  # Same for singular/plural
        else:
            plural = 'user(s)'  # Fallback
        
        return f"{formatted_number} {plural}"
    
    def sort_names(self, names):
        """Sort names according to locale"""
        return self.collator.sort(names)
    
    def format_last_seen(self, datetime_obj):
        """Format last seen date"""
        return f"Last seen: {self.date_formatter.format(datetime_obj)}"

# Example usage
from datetime import datetime, timedelta

ui_en = LocalizedUI('en-US')
ui_de = LocalizedUI('de-DE')

# Format user count
count = 1234
print(f"English: {ui_en.format_user_count(count)}")
print(f"German: {ui_de.format_user_count(count)}")

# Sort names
names = ['Müller', 'Smith', 'Zöller', 'Anderson']
print(f"English sort: {ui_en.sort_names(names)}")
print(f"German sort: {ui_de.sort_names(names)}")

# Format dates
last_week = datetime.now() - timedelta(days=7)
print(f"English: {ui_en.format_last_seen(last_week)}")
print(f"German: {ui_de.format_last_seen(last_week)}")
```

### Content Localization

```python
def localized_search(query, documents, locale_id):
    """Locale-aware document search"""
    collator = uicu.Collator(locale_id)
    collator.set_strength('primary')  # Ignore case and accents
    
    matches = []
    for doc_id, content in documents.items():
        # Simple substring search with locale-aware comparison
        words = content.lower().split()
        for word in words:
            if collator.compare(word, query.lower()) == 0:
                matches.append((doc_id, content))
                break
    
    return matches

# Example documents
documents = {
    1: "The café serves excellent coffee",
    2: "This cafe has great atmosphere", 
    3: "Restaurant menu includes cafés",
    4: "Coffee shop and café combined",
}

# Search for "cafe" - should match all variations
results = localized_search("cafe", documents, 'en-US')
print("Search results for 'cafe':")
for doc_id, content in results:
    print(f"  {doc_id}: {content}")
```

### Input Validation

```python
def validate_postal_code(code, locale_id):
    """Validate postal code format by locale"""
    locale = uicu.Locale(locale_id)
    country = locale.country
    
    # Simple validation patterns (real apps would use comprehensive rules)
    patterns = {
        'US': r'^\d{5}(-\d{4})?$',          # 12345 or 12345-6789
        'CA': r'^[A-Z]\d[A-Z] \d[A-Z]\d$',  # A1A 1A1
        'GB': r'^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$',  # SW1A 1AA
        'DE': r'^\d{5}$',                    # 12345
        'JP': r'^\d{3}-\d{4}$',             # 123-4567
    }
    
    import re
    pattern = patterns.get(country)
    if not pattern:
        return False, f"No validation rule for {locale.country_display_name}"
    
    if re.match(pattern, code):
        return True, "Valid postal code"
    else:
        return False, f"Invalid postal code for {locale.country_display_name}"

# Test postal codes
test_codes = [
    ('12345', 'en-US'),
    ('K1A 0A6', 'en-CA'),
    ('SW1A 1AA', 'en-GB'),
    ('10117', 'de-DE'),
    ('123-4567', 'ja-JP'),
]

for code, locale_id in test_codes:
    valid, message = validate_postal_code(code, locale_id)
    locale = uicu.Locale(locale_id)
    print(f"{code} ({locale.country_display_name}): {message}")
```

## Performance and Caching

### Efficient Locale Usage

```python
import time

def benchmark_locale_operations():
    """Benchmark locale-intensive operations"""
    
    # Create collators for different locales
    locales = ['en-US', 'de-DE', 'fr-FR', 'ja-JP', 'ar-SA']
    collators = {}
    
    start = time.time()
    for locale_id in locales:
        collators[locale_id] = uicu.Collator(locale_id)
    creation_time = time.time() - start
    
    # Perform comparisons
    test_pairs = [('café', 'cafe'), ('Müller', 'Mueller'), ('naïve', 'naive')] * 1000
    
    start = time.time()
    for locale_id, collator in collators.items():
        for text1, text2 in test_pairs:
            result = collator.compare(text1, text2)
    comparison_time = time.time() - start
    
    print(f"Collator creation: {creation_time:.4f}s")
    print(f"Comparisons: {comparison_time:.4f}s")
    print(f"Total operations: {len(locales) * len(test_pairs)}")

benchmark_locale_operations()
```

## Next Steps

Now that you understand locale management:

1. **[Text Collation](text-collation.md)** - Deep dive into locale-aware sorting
2. **[Date-Time Formatting](date-time-formatting.md)** - Comprehensive formatting guide
3. **[Text Segmentation](text-segmentation.md)** - Locale-aware text breaking
4. **[API Reference](../api/locale.md)** - Complete Locale class documentation

!!! tip "Locale Caching"
    UICU caches locale objects and their associated services (collators, formatters) for optimal performance.

Ready to master text sorting and comparison? Continue to [Text Collation](text-collation.md)!