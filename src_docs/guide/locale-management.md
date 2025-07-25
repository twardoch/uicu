# Locale Management

Locales are at the heart of internationalization in UICU. They define language, regional, and cultural conventions that affect text processing, formatting, and display.

## Understanding Locales

A locale combines:
- **Language**: The primary language (e.g., 'en' for English)
- **Region**: Country or region (e.g., 'US' for United States)
- **Script**: Writing system (e.g., 'Latn' for Latin script)
- **Variants**: Additional variations (e.g., 'POSIX')

```python
import uicu

# Create locales in different ways
locale1 = uicu.Locale('en-US')          # Language tag
locale2 = uicu.Locale('zh_Hant_TW')     # Underscore separator
locale3 = uicu.Locale('sr-Cyrl-RS')     # With script

# Access locale components
print(f"Language: {locale1.language}")   # 'en'
print(f"Region: {locale1.region}")       # 'US'
print(f"Script: {locale3.script}")       # 'Cyrl'
```

## Creating and Using Locales

### Basic Locale Creation

```python
# Different locale formats
locales = [
    uicu.Locale('en'),              # Language only
    uicu.Locale('en-US'),           # Language + Region
    uicu.Locale('zh-Hant'),         # Language + Script
    uicu.Locale('zh-Hant-TW'),      # Language + Script + Region
    uicu.Locale('en-US-POSIX'),     # With variant
]

for locale in locales:
    print(f"{locale.language_tag:15} -> {locale.display_name}")
```

### System Default Locale

```python
# Get system's default locale
default = uicu.get_default_locale()
print(f"System locale: {default.language_tag}")
print(f"Display name: {default.display_name}")

# Get display name in different languages
print(f"In French: {default.get_display_name('fr')}")
print(f"In Japanese: {default.get_display_name('ja')}")
print(f"In Arabic: {default.get_display_name('ar')}")
```

### Available Locales

```python
# List all available locales
available = uicu.get_available_locales()
print(f"Total available locales: {len(available)}")

# Show a sample
print("\nSample locales:")
for locale in sorted(available)[:10]:
    loc = uicu.Locale(locale)
    print(f"  {locale:10} -> {loc.display_name}")

# Find locales for a specific language
spanish_locales = [loc for loc in available if loc.startswith('es')]
print(f"\nSpanish locales ({len(spanish_locales)}):")
for locale in sorted(spanish_locales)[:5]:
    loc = uicu.Locale(locale)
    print(f"  {locale:10} -> {loc.display_name}")
```

## Locale Components

### Language, Script, and Region

```python
# Analyze locale components
def analyze_locale(locale_id: str):
    locale = uicu.Locale(locale_id)
    print(f"\nLocale: {locale_id}")
    print(f"  Language: {locale.language} ({locale.get_display_language()})")
    print(f"  Script: {locale.script or 'default'} ({locale.get_display_script() or 'default'})")
    print(f"  Region: {locale.region or 'none'} ({locale.get_display_region() or 'none'})")
    print(f"  Variant: {locale.variant or 'none'} ({locale.get_display_variant() or 'none'})")
    print(f"  Full name: {locale.display_name}")

# Examples
analyze_locale('en-US')
analyze_locale('zh-Hant-TW')
analyze_locale('sr-Cyrl-RS')
analyze_locale('en-US-POSIX')
```

### BCP 47 Language Tags

UICU supports standard BCP 47 language tags:

```python
# Work with BCP 47 tags
bcp47_examples = [
    'en-US',           # Simple language-region
    'zh-Hans-CN',      # With script
    'es-419',          # Region code (Latin America)
    'en-GB-oxendict',  # Oxford English Dictionary spelling
    'ja-JP-u-ca-japanese',  # With Unicode extension
]

for tag in bcp47_examples:
    locale = uicu.Locale(tag)
    print(f"{tag:20} -> {locale.display_name}")
```

## Locale-Aware Services

Locales serve as factories for locale-specific services:

### Creating Collators

```python
# Create locale-specific collators
locale_en = uicu.Locale('en-US')
locale_de = uicu.Locale('de-DE')
locale_sv = uicu.Locale('sv-SE')

# Get collators from locales
collator_en = locale_en.get_collator()
collator_de = locale_de.get_collator()
collator_sv = locale_sv.get_collator()

# Compare sorting differences
words = ['öl', 'ol', 'őr']
print(f"English sort: {collator_en.sort(words)}")
print(f"German sort: {collator_de.sort(words)}")
print(f"Swedish sort: {collator_sv.sort(words)}")
```

### Creating Formatters

```python
from datetime import datetime

# Create locale-specific date formatters
locales = ['en-US', 'fr-FR', 'ja-JP', 'ar-SA']
date = datetime.now()

for locale_id in locales:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_datetime_formatter(
        date_style='full',
        time_style='short'
    )
    formatted = formatter.format(date)
    print(f"{locale_id}: {formatted}")
```

## Locale Hierarchies and Fallbacks

Locales follow a hierarchy for resource lookup:

```python
# Locale fallback chain
def show_fallback_chain(locale_id: str):
    locale = uicu.Locale(locale_id)
    print(f"\nFallback chain for {locale_id}:")
    
    # Simplified fallback demonstration
    parts = locale_id.split('-')
    while parts:
        print(f"  -> {'-'.join(parts)}")
        parts.pop()
    print("  -> root")

# Examples
show_fallback_chain('zh-Hant-TW')  # Traditional Chinese (Taiwan)
show_fallback_chain('en-GB-oxendict')  # British English (Oxford)
```

## Display Names and Translations

Get locale information in different languages:

```python
# Display locale names in various languages
locale_to_describe = uicu.Locale('ja-JP')

display_languages = [
    ('en', 'English'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('zh', 'Chinese'),
    ('ar', 'Arabic'),
    ('ru', 'Russian'),
    ('ja', 'Japanese'),
]

print(f"Describing locale: {locale_to_describe.language_tag}\n")
for lang_code, lang_name in display_languages:
    name = locale_to_describe.get_display_name(lang_code)
    print(f"{lang_name:10} {name}")
```

## Language and Region Codes

### ISO Language Codes

```python
# Common ISO 639 language codes
language_samples = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('zh', 'Chinese'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('pt', 'Portuguese'),
    ('ru', 'Russian'),
    ('ja', 'Japanese'),
    ('de', 'German'),
    ('fr', 'French'),
]

print("ISO 639 Language Codes:")
for code, expected in language_samples:
    locale = uicu.Locale(code)
    print(f"  {code}: {locale.get_display_language()} (expected: {expected})")
```

### ISO Country/Region Codes

```python
# Common ISO 3166 country codes
region_samples = [
    ('US', 'United States'),
    ('GB', 'United Kingdom'),
    ('CN', 'China'),
    ('JP', 'Japan'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('BR', 'Brazil'),
    ('IN', 'India'),
    ('419', 'Latin America'),  # UN M.49 code
]

print("\nISO 3166 Country/Region Codes:")
for code, expected in region_samples:
    locale = uicu.Locale(f"en-{code}")
    print(f"  {code}: {locale.get_display_region()} (expected: {expected})")
```

## Script Codes

```python
# ISO 15924 script codes
script_samples = [
    ('Latn', 'Latin', 'en'),
    ('Cyrl', 'Cyrillic', 'ru'),
    ('Arab', 'Arabic', 'ar'),
    ('Hani', 'Han (Chinese)', 'zh'),
    ('Jpan', 'Japanese', 'ja'),
    ('Deva', 'Devanagari', 'hi'),
    ('Hebr', 'Hebrew', 'he'),
    ('Thai', 'Thai', 'th'),
]

print("ISO 15924 Script Codes:")
for script, expected, lang in script_samples:
    locale = uicu.Locale(f"{lang}-{script}")
    print(f"  {script}: {locale.get_display_script()} (expected: {expected})")
```

## Practical Examples

### Multi-Language Application

```python
class MultilingualApp:
    """Example of locale-aware application."""
    
    def __init__(self, default_locale='en-US'):
        self.current_locale = uicu.Locale(default_locale)
        self.translations = {
            'en': {
                'welcome': 'Welcome',
                'goodbye': 'Goodbye',
                'today': 'Today is',
            },
            'es': {
                'welcome': 'Bienvenido',
                'goodbye': 'Adiós',
                'today': 'Hoy es',
            },
            'fr': {
                'welcome': 'Bienvenue',
                'goodbye': 'Au revoir',
                'today': "Aujourd'hui c'est",
            },
            'ja': {
                'welcome': 'ようこそ',
                'goodbye': 'さようなら',
                'today': '今日は',
            },
        }
    
    def set_locale(self, locale_id: str):
        """Change application locale."""
        self.current_locale = uicu.Locale(locale_id)
    
    def translate(self, key: str) -> str:
        """Get translated string."""
        lang = self.current_locale.language
        return self.translations.get(lang, self.translations['en']).get(key, key)
    
    def format_date(self, date: datetime) -> str:
        """Format date according to current locale."""
        formatter = self.current_locale.get_datetime_formatter(date_style='full')
        return formatter.format(date)
    
    def display_welcome(self):
        """Show localized welcome message."""
        welcome = self.translate('welcome')
        today = self.translate('today')
        date = self.format_date(datetime.now())
        print(f"{welcome}! {today} {date}")

# Use the application
app = MultilingualApp()

for locale_id in ['en-US', 'es-ES', 'fr-FR', 'ja-JP']:
    print(f"\n--- Locale: {locale_id} ---")
    app.set_locale(locale_id)
    app.display_welcome()
```

### Locale-Aware Sorting

```python
def demonstrate_locale_sorting():
    """Show how locale affects sorting."""
    # Names with special characters
    names = ['Müller', 'Mueller', 'Muller', 'Mūller', 'Mueller']
    
    locales_to_test = [
        ('en-US', 'English (US)'),
        ('de-DE', 'German'),
        ('sv-SE', 'Swedish'),
    ]
    
    print("Sorting names with different locale rules:\n")
    print(f"Names to sort: {names}\n")
    
    for locale_id, desc in locales_to_test:
        locale = uicu.Locale(locale_id)
        collator = locale.get_collator()
        sorted_names = collator.sort(names)
        print(f"{desc:15} {sorted_names}")

demonstrate_locale_sorting()
```

### Currency and Number Formatting

```python
# Locale-specific number formatting (preview of future features)
def format_currency_preview(amount: float, locale_id: str):
    """Preview of currency formatting (coming in v2.0)."""
    locale = uicu.Locale(locale_id)
    
    # Get currency symbol (simplified)
    currency_symbols = {
        'en-US': '$',
        'en-GB': '£',
        'de-DE': '€',
        'ja-JP': '¥',
        'ar-SA': 'ر.س',
    }
    
    symbol = currency_symbols.get(locale_id, '$')
    
    # Simplified formatting
    if locale_id.startswith('en'):
        return f"{symbol}{amount:,.2f}"
    elif locale_id == 'de-DE':
        return f"{amount:,.2f} {symbol}".replace(',', 'X').replace('.', ',').replace('X', '.')
    else:
        return f"{symbol} {amount:,.2f}"

# Examples
amounts = [1234.56, 9999.99, 0.99]
locales = ['en-US', 'en-GB', 'de-DE', 'ja-JP']

print("Currency formatting preview (full support in v2.0):")
for amount in amounts:
    print(f"\nAmount: {amount}")
    for locale_id in locales:
        formatted = format_currency_preview(amount, locale_id)
        print(f"  {locale_id}: {formatted}")
```

## Best Practices

### 1. Locale Selection

```python
def select_best_locale(user_preferences: list, available: list) -> str:
    """Select best matching locale from user preferences."""
    # Direct match
    for pref in user_preferences:
        if pref in available:
            return pref
    
    # Language-only match
    for pref in user_preferences:
        lang = pref.split('-')[0]
        for avail in available:
            if avail.startswith(lang):
                return avail
    
    # Default fallback
    return 'en-US'

# Example
user_prefs = ['es-MX', 'es', 'en']
available_locales = ['en-US', 'en-GB', 'es-ES', 'fr-FR']
best = select_best_locale(user_prefs, available_locales)
print(f"Best match: {best}")
```

### 2. Caching Locale Objects

```python
class LocaleCache:
    """Cache locale objects for performance."""
    
    def __init__(self):
        self._cache = {}
    
    def get_locale(self, locale_id: str) -> uicu.Locale:
        if locale_id not in self._cache:
            self._cache[locale_id] = uicu.Locale(locale_id)
        return self._cache[locale_id]
    
    def get_collator(self, locale_id: str, **kwargs) -> uicu.Collator:
        key = (locale_id, tuple(sorted(kwargs.items())))
        if key not in self._cache:
            locale = self.get_locale(locale_id)
            self._cache[key] = locale.get_collator(**kwargs)
        return self._cache[key]

# Use the cache
cache = LocaleCache()
collator1 = cache.get_collator('en-US')
collator2 = cache.get_collator('en-US')  # Returns cached instance
print(f"Same object: {collator1 is collator2}")
```

### 3. Handling Unknown Locales

```python
def safe_create_locale(locale_id: str, fallback='en-US') -> uicu.Locale:
    """Safely create locale with fallback."""
    try:
        # Try to create the requested locale
        locale = uicu.Locale(locale_id)
        
        # Verify it's valid by checking if it has a display name
        if locale.display_name:
            return locale
    except Exception:
        pass
    
    # Fallback
    print(f"Warning: Unknown locale '{locale_id}', using '{fallback}'")
    return uicu.Locale(fallback)

# Test with various locale IDs
test_locales = ['en-US', 'xx-YY', 'de-DE', 'invalid', 'zh-TW']
for locale_id in test_locales:
    locale = safe_create_locale(locale_id)
    print(f"{locale_id:10} -> {locale.language_tag} ({locale.display_name})")
```

## Performance Considerations

1. **Cache Locale objects** - They're expensive to create
2. **Reuse service objects** - Collators, formatters, etc.
3. **Use locale IDs directly** when possible instead of parsing
4. **Batch operations** using the same locale

```python
import time

# Performance comparison
iterations = 10000

# Method 1: Create new locale each time (slow)
start = time.time()
for i in range(iterations):
    locale = uicu.Locale('en-US')
    collator = locale.get_collator()
elapsed1 = time.time() - start

# Method 2: Reuse locale and collator (fast)
start = time.time()
locale = uicu.Locale('en-US')
collator = locale.get_collator()
for i in range(iterations):
    # Use existing collator
    pass
elapsed2 = time.time() - start

print(f"Create each time: {elapsed1:.3f}s")
print(f"Reuse objects: {elapsed2:.3f}s")
print(f"Speedup: {elapsed1/elapsed2:.1f}x")
```

## Next Steps

- Learn about [Text Collation](text-collation.md) for locale-aware sorting
- Explore [Text Segmentation](text-segmentation.md) with locale rules
- Master [Date/Time Formatting](date-time-formatting.md) for different locales