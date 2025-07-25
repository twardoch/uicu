# uicu.locale

Locale management and locale-aware service creation.

This module provides BCP 47 compliant locale handling with factory methods for creating locale-specific services like collators and formatters.

## Classes

### `Locale`

::: uicu.locale.Locale

## Functions

### `get_default_locale`

::: uicu.locale.get_default_locale

### `get_available_locales`

::: uicu.locale.get_available_locales

## Examples

### Basic Locale Usage

```python
from uicu import Locale

# Create locale from tag
locale = Locale('en-US')
print(f"Language: {locale.language}")
print(f"Region: {locale.region}")
print(f"Display name: {locale.display_name}")

# Create locale with script
locale_script = Locale('zh-Hant-TW')
print(f"Script: {locale_script.script}")
print(f"Full tag: {locale_script.language_tag}")
```

### Locale Components

```python
# Access all locale components
locale = Locale('en-US-POSIX')
print(f"Language: {locale.language}")
print(f"Script: {locale.script}")  # None for default script
print(f"Region: {locale.region}")
print(f"Variant: {locale.variant}")

# Get display names in different languages
print(f"English: {locale.get_display_name('en')}")
print(f"French: {locale.get_display_name('fr')}")
print(f"Spanish: {locale.get_display_name('es')}")
```

### Factory Methods

```python
# Create locale-specific services
locale = Locale('de-DE')

# Create collator
collator = locale.get_collator(strength='primary')
sorted_words = collator.sort(['Müller', 'Mueller', 'Muller'])

# Create date formatter
formatter = locale.get_datetime_formatter(
    date_style='full',
    time_style='short'
)
formatted = formatter.format(datetime.now())
```

### System Locale

```python
# Get system default
default = get_default_locale()
print(f"System locale: {default.language_tag}")
print(f"Display name: {default.display_name}")

# Get all available locales
available = get_available_locales()
print(f"Available locales: {len(available)}")

# Find Spanish locales
spanish = [loc for loc in available if loc.startswith('es')]
print(f"Spanish variants: {spanish}")
```

### Locale Parsing

```python
# Different locale formats are accepted
locales = [
    'en',              # Language only
    'en-US',           # Language-Region
    'zh-Hans',         # Language-Script
    'zh-Hans-CN',      # Language-Script-Region
    'en-US-POSIX',     # With variant
    'sr-Cyrl-RS',      # Serbian Cyrillic
]

for locale_id in locales:
    locale = Locale(locale_id)
    print(f"{locale_id:15} → {locale.display_name}")
```

### Display Names

```python
locale = Locale('ja-JP')

# Get component display names
print(f"Language: {locale.get_display_language()}")  # In same locale
print(f"Language (EN): {locale.get_display_language('en')}")  # In English
print(f"Region: {locale.get_display_region()}")
print(f"Script: {locale.get_display_script()}")

# Full display name in various languages
languages = ['en', 'fr', 'de', 'es', 'zh', 'ar']
for lang in languages:
    name = locale.get_display_name(lang)
    print(f"{lang}: {name}")
```

## Locale Identifiers

### BCP 47 Language Tags

UICU supports standard BCP 47 language tags:

- `en` - English
- `en-US` - English (United States)
- `en-GB` - English (United Kingdom)
- `zh-Hans` - Chinese (Simplified)
- `zh-Hant-TW` - Chinese (Traditional, Taiwan)
- `sr-Cyrl` - Serbian (Cyrillic)
- `sr-Latn` - Serbian (Latin)

### Common Locale Codes

| Language | Code | Example Full Locale |
|----------|------|-------------------|
| English | en | en-US, en-GB |
| Spanish | es | es-ES, es-MX |
| French | fr | fr-FR, fr-CA |
| German | de | de-DE, de-CH |
| Chinese | zh | zh-CN, zh-TW |
| Japanese | ja | ja-JP |
| Korean | ko | ko-KR |
| Arabic | ar | ar-SA, ar-EG |
| Russian | ru | ru-RU |
| Portuguese | pt | pt-BR, pt-PT |

### Script Codes (ISO 15924)

| Script | Code | Example |
|--------|------|---------|
| Latin | Latn | en-Latn |
| Cyrillic | Cyrl | ru-Cyrl |
| Arabic | Arab | ar-Arab |
| Simplified Chinese | Hans | zh-Hans |
| Traditional Chinese | Hant | zh-Hant |
| Devanagari | Deva | hi-Deva |

### Region Codes (ISO 3166)

| Region | Code | Name |
|--------|------|------|
| United States | US | |
| United Kingdom | GB | |
| Germany | DE | |
| France | FR | |
| China | CN | |
| Japan | JP | |
| Brazil | BR | |
| India | IN | |
| 419 | 419 | Latin America |

## Advanced Usage

### Locale Matching

```python
def find_best_locale(user_preferences, available_locales):
    """Find best matching locale from user preferences."""
    for pref in user_preferences:
        # Exact match
        if pref in available_locales:
            return Locale(pref)
        
        # Try language-only match
        lang = pref.split('-')[0]
        for avail in available_locales:
            if avail.startswith(lang + '-'):
                return Locale(avail)
    
    # Default fallback
    return Locale('en-US')

# Example
user_prefs = ['es-MX', 'es', 'en']
available = ['en-US', 'en-GB', 'es-ES', 'fr-FR']
best = find_best_locale(user_prefs, available)
print(f"Best match: {best.language_tag}")
```

### Locale Hierarchies

```python
# Create locale chain for fallback
def get_locale_chain(locale_id):
    """Get locale fallback chain."""
    chain = []
    locale = Locale(locale_id)
    
    # Full locale
    chain.append(locale)
    
    # Language + Script
    if locale.script and locale.region:
        chain.append(Locale(f"{locale.language}-{locale.script}"))
    
    # Language only
    if locale.language != locale_id:
        chain.append(Locale(locale.language))
    
    # Root locale
    chain.append(Locale('root'))
    
    return chain

# Example
chain = get_locale_chain('zh-Hant-TW')
for loc in chain:
    print(f"→ {loc.language_tag}: {loc.display_name}")
```

### Custom Locale Data

```python
class LocaleRegistry:
    """Registry for application-specific locale data."""
    
    def __init__(self):
        self.custom_names = {
            'en-US': 'American English',
            'en-GB': 'British English',
            'zh-CN': 'Simplified Chinese',
            'zh-TW': 'Traditional Chinese',
        }
    
    def get_custom_name(self, locale_id):
        """Get custom display name."""
        return self.custom_names.get(locale_id, 
                                   Locale(locale_id).display_name)
    
    def get_writing_direction(self, locale_id):
        """Get locale's primary writing direction."""
        locale = Locale(locale_id)
        if locale.language in ['ar', 'he', 'fa', 'ur']:
            return 'rtl'
        return 'ltr'

# Usage
registry = LocaleRegistry()
print(registry.get_custom_name('en-US'))
print(registry.get_writing_direction('ar-SA'))
```

## Performance Notes

1. **Locale Caching**: Locale objects are lightweight but should still be cached when used repeatedly.

2. **Factory Methods**: Services created via factory methods (get_collator, etc.) should be reused.

3. **Available Locales**: The list of available locales is cached after first access.

## Error Handling

```python
# Invalid locale handling
try:
    locale = Locale('invalid-locale-tag')
except Exception as e:
    print(f"Error: {e}")
    # Use fallback
    locale = Locale('en-US')

# Safe locale creation with fallback
def safe_locale(locale_id, fallback='en-US'):
    try:
        return Locale(locale_id)
    except Exception:
        return Locale(fallback)
```

## Thread Safety

Locale objects are immutable and thread-safe. Services created from locales (collators, formatters) are thread-safe for read operations.

## See Also

- [Locale Management Guide](../guide/locale-management.md) - Detailed usage guide
- [`uicu.collate`](collate.md) - Locale-aware text collation
- [`uicu.format`](format.md) - Locale-aware formatting