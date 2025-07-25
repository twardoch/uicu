# Best Practices

This guide covers best practices for using UICU effectively in your applications, including performance optimization, error handling, and internationalization patterns.

## Performance Optimization

### Reuse Expensive Objects

ICU objects like collators, formatters, and transliterators are expensive to create. Always reuse them:

```python
import uicu
from datetime import datetime

# ❌ Bad: Creating objects repeatedly
def bad_format_dates(dates, locale='en-US'):
    results = []
    for date in dates:
        formatter = uicu.DateTimeFormatter(locale)  # Expensive!
        results.append(formatter.format(date))
    return results

# ✅ Good: Reuse formatter
def good_format_dates(dates, locale='en-US'):
    formatter = uicu.DateTimeFormatter(locale)  # Create once
    return [formatter.format(date) for date in dates]

# Performance comparison
dates = [datetime.now() for _ in range(1000)]
import time

start = time.time()
bad_format_dates(dates)
bad_time = time.time() - start

start = time.time()
good_format_dates(dates)
good_time = time.time() - start

print(f"Bad: {bad_time:.3f}s, Good: {good_time:.3f}s")
print(f"Speedup: {bad_time/good_time:.1f}x")
```

### Use Object Pools

For applications that need many different configurations:

```python
class UICUObjectPool:
    """Pool of reusable UICU objects."""
    
    def __init__(self):
        self._collators = {}
        self._formatters = {}
        self._transliterators = {}
        self._segmenters = {}
    
    def get_collator(self, locale='en-US', **kwargs):
        key = (locale, tuple(sorted(kwargs.items())))
        if key not in self._collators:
            self._collators[key] = uicu.Collator(locale, **kwargs)
        return self._collators[key]
    
    def get_formatter(self, locale='en-US', **kwargs):
        key = (locale, tuple(sorted(kwargs.items())))
        if key not in self._formatters:
            self._formatters[key] = uicu.DateTimeFormatter(locale, **kwargs)
        return self._formatters[key]
    
    def get_transliterator(self, transform_id):
        if transform_id not in self._transliterators:
            self._transliterators[transform_id] = uicu.Transliterator(transform_id)
        return self._transliterators[transform_id]
    
    def get_word_segmenter(self, locale='en-US'):
        if locale not in self._segmenters:
            self._segmenters[locale] = uicu.WordSegmenter(locale)
        return self._segmenters[locale]

# Global pool for application
pool = UICUObjectPool()

# Usage throughout application
def process_text(text, locale='en-US'):
    collator = pool.get_collator(locale)
    segmenter = pool.get_word_segmenter(locale)
    # ... use cached objects
```

### Batch Operations

Process multiple items together:

```python
# ❌ Bad: Individual operations
def bad_sort_lists(lists_of_names, locale='en-US'):
    results = []
    for names in lists_of_names:
        collator = uicu.Collator(locale)
        sorted_names = collator.sort(names)
        results.append(sorted_names)
    return results

# ✅ Good: Batch processing
def good_sort_lists(lists_of_names, locale='en-US'):
    collator = uicu.Collator(locale)
    return [collator.sort(names) for names in lists_of_names]

# ✅ Better: Pre-compute sort keys for very large datasets
def best_sort_large_list(items, locale='en-US'):
    collator = uicu.Collator(locale)
    # Pre-compute sort keys
    keyed_items = [(item, collator.get_sort_key(item)) for item in items]
    # Sort by pre-computed keys
    keyed_items.sort(key=lambda x: x[1])
    # Extract sorted items
    return [item for item, key in keyed_items]
```

## Error Handling

### Graceful Degradation

Always handle potential errors gracefully:

```python
def safe_char_info(char):
    """Get character info with fallback."""
    try:
        c = uicu.Char(char)
        return {
            'name': c.name,
            'category': c.category,
            'script': c.script,
            'error': None
        }
    except uicu.UICUError as e:
        # Fallback to basic Python info
        return {
            'name': f'U+{ord(char):04X}' if len(char) == 1 else 'Invalid',
            'category': 'Unknown',
            'script': 'Unknown',
            'error': str(e)
        }

# Test with various inputs
test_chars = ['A', '€', '🎉', 'Invalid string', '']
for char in test_chars:
    info = safe_char_info(char)
    print(f"{char!r}: {info['name']} ({info['category']})")
    if info['error']:
        print(f"  Error: {info['error']}")
```

### Locale Fallbacks

Handle missing or invalid locales:

```python
class LocaleManager:
    """Manage locales with fallback support."""
    
    def __init__(self, fallback='en-US'):
        self.fallback = fallback
        self._locale_cache = {}
    
    def get_locale(self, locale_id):
        """Get locale with fallback."""
        if locale_id in self._locale_cache:
            return self._locale_cache[locale_id]
        
        try:
            locale = uicu.Locale(locale_id)
            # Verify locale is valid
            if locale.language:
                self._locale_cache[locale_id] = locale
                return locale
        except Exception:
            pass
        
        # Fallback
        print(f"Warning: Invalid locale '{locale_id}', using '{self.fallback}'")
        if self.fallback not in self._locale_cache:
            self._locale_cache[self.fallback] = uicu.Locale(self.fallback)
        return self._locale_cache[self.fallback]
    
    def get_best_locale(self, preferences, available):
        """Find best matching locale from preferences."""
        for pref in preferences:
            # Exact match
            if pref in available:
                return self.get_locale(pref)
            
            # Language-only match
            lang = pref.split('-')[0]
            for avail in available:
                if avail.startswith(lang):
                    return self.get_locale(avail)
        
        # Fallback
        return self.get_locale(self.fallback)

# Example usage
manager = LocaleManager()
locale = manager.get_locale('invalid-locale')
print(f"Got locale: {locale.language_tag}")
```

### Input Validation

Always validate user input:

```python
def validate_and_process_text(text, operation='sort', locale='en-US'):
    """Validate input before processing."""
    # Input validation
    if not isinstance(text, (str, list)):
        raise TypeError(f"Expected str or list, got {type(text)}")
    
    if isinstance(text, str):
        if not text:
            return text  # Empty string
        
        # Validate string doesn't contain problematic characters
        if '\x00' in text:
            text = text.replace('\x00', '')  # Remove null bytes
    
    elif isinstance(text, list):
        if not text:
            return text  # Empty list
        
        # Validate all items are strings
        if not all(isinstance(item, str) for item in text):
            raise TypeError("All list items must be strings")
    
    # Process based on operation
    if operation == 'sort' and isinstance(text, list):
        collator = uicu.Collator(locale)
        return collator.sort(text)
    elif operation == 'words' and isinstance(text, str):
        return list(uicu.words(text, locale=locale))
    else:
        return text

# Test with various inputs
try:
    print(validate_and_process_text(['banana', 'apple'], 'sort'))
    print(validate_and_process_text('Hello world', 'words'))
    print(validate_and_process_text(['not', 'all', 123, 'strings'], 'sort'))
except Exception as e:
    print(f"Error: {e}")
```

## Internationalization Patterns

### Locale-Aware Application Structure

```python
class I18nApplication:
    """Base class for internationalized applications."""
    
    def __init__(self, default_locale='en-US'):
        self.default_locale = default_locale
        self.current_locale = None
        self.pool = UICUObjectPool()
        self.translations = {}
        
        # Initialize with default locale
        self.set_locale(default_locale)
    
    def set_locale(self, locale_id):
        """Change application locale."""
        try:
            self.current_locale = uicu.Locale(locale_id)
        except Exception:
            print(f"Invalid locale '{locale_id}', using default")
            self.current_locale = uicu.Locale(self.default_locale)
    
    def get_collator(self, **kwargs):
        """Get collator for current locale."""
        return self.pool.get_collator(self.current_locale.language_tag, **kwargs)
    
    def get_formatter(self, **kwargs):
        """Get formatter for current locale."""
        return self.pool.get_formatter(self.current_locale.language_tag, **kwargs)
    
    def format_date(self, date, style='medium'):
        """Format date in current locale."""
        formatter = self.get_formatter(date_style=style)
        return formatter.format(date)
    
    def sort_list(self, items, **kwargs):
        """Sort list according to current locale."""
        collator = self.get_collator(**kwargs)
        return collator.sort(items)
    
    def translate(self, key, **kwargs):
        """Get translated string (placeholder)."""
        # In real app, load from translation files
        lang = self.current_locale.language
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key].format(**kwargs)
        return key

# Example usage
app = I18nApplication()

# Switch locales
for locale in ['en-US', 'de-DE', 'ja-JP']:
    app.set_locale(locale)
    print(f"\nLocale: {app.current_locale.display_name}")
    
    # Use locale-aware features
    names = ['Müller', 'Mueller', 'André', 'Andrew']
    sorted_names = app.sort_list(names)
    print(f"  Sorted names: {sorted_names}")
    
    date = datetime.now()
    formatted = app.format_date(date, style='full')
    print(f"  Date: {formatted}")
```

### User Preference Detection

```python
def detect_user_preferences():
    """Detect user's locale preferences."""
    preferences = []
    
    # 1. Check environment variables
    import os
    for var in ['LC_ALL', 'LC_MESSAGES', 'LANG']:
        if var in os.environ:
            locale_str = os.environ[var]
            # Extract locale part (before .UTF-8, etc.)
            locale_id = locale_str.split('.')[0].replace('_', '-')
            if locale_id and locale_id != 'C':
                preferences.append(locale_id)
    
    # 2. Check system default
    try:
        system_locale = uicu.get_default_locale()
        preferences.append(system_locale.language_tag)
    except Exception:
        pass
    
    # 3. Add fallbacks
    if not preferences:
        preferences.append('en-US')
    
    # Remove duplicates while preserving order
    seen = set()
    unique_prefs = []
    for pref in preferences:
        if pref not in seen:
            seen.add(pref)
            unique_prefs.append(pref)
    
    return unique_prefs

# Example
prefs = detect_user_preferences()
print(f"User preferences: {prefs}")
```

## Memory Management

### Clean Up Large Operations

```python
def process_large_dataset(file_path, locale='en-US'):
    """Process large dataset with proper cleanup."""
    collator = uicu.Collator(locale)
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            batch = []
            batch_size = 1000
            
            for line in f:
                batch.append(line.strip())
                
                if len(batch) >= batch_size:
                    # Process batch
                    sorted_batch = collator.sort(batch)
                    results.extend(sorted_batch)
                    
                    # Clear batch
                    batch = []
            
            # Process remaining
            if batch:
                sorted_batch = collator.sort(batch)
                results.extend(sorted_batch)
        
        return results
    
    finally:
        # Cleanup if needed
        pass
```

### Lazy Loading

```python
class LazyUICULoader:
    """Lazy load UICU objects as needed."""
    
    def __init__(self, locale='en-US'):
        self.locale = locale
        self._collator = None
        self._formatter = None
        self._word_segmenter = None
    
    @property
    def collator(self):
        if self._collator is None:
            self._collator = uicu.Collator(self.locale)
        return self._collator
    
    @property
    def formatter(self):
        if self._formatter is None:
            self._formatter = uicu.DateTimeFormatter(self.locale)
        return self._formatter
    
    @property
    def word_segmenter(self):
        if self._word_segmenter is None:
            self._word_segmenter = uicu.WordSegmenter(self.locale)
        return self._word_segmenter
    
    def reset(self):
        """Reset all cached objects."""
        self._collator = None
        self._formatter = None
        self._word_segmenter = None

# Usage
loader = LazyUICULoader('en-US')

# Objects created only when accessed
if need_sorting:
    sorted_items = loader.collator.sort(items)

if need_formatting:
    formatted = loader.formatter.format(date)
```

## Testing Strategies

### Test with Diverse Data

```python
import unittest

class TestUICUWithDiverseData(unittest.TestCase):
    """Test UICU with diverse Unicode data."""
    
    def setUp(self):
        self.test_strings = [
            # ASCII
            "Hello World",
            # European
            "Café résumé naïve",
            # Cyrillic
            "Привет мир",
            # CJK
            "你好世界",
            "こんにちは",
            "안녕하세요",
            # Arabic (RTL)
            "مرحبا بالعالم",
            # Emoji
            "Hello 👋 🌍",
            # Complex graphemes
            "👨‍👩‍👧‍👦",
            # Mixed scripts
            "Hello мир 世界",
        ]
    
    def test_grapheme_segmentation(self):
        """Test grapheme segmentation with diverse data."""
        for text in self.test_strings:
            graphemes = list(uicu.graphemes(text))
            # Should not raise exceptions
            self.assertIsInstance(graphemes, list)
            
            # Special case: family emoji
            if "👨‍👩‍👧‍👦" in text:
                self.assertIn("👨‍👩‍👧‍👦", graphemes)
    
    def test_collation(self):
        """Test collation doesn't break with diverse data."""
        collator = uicu.Collator('en-US')
        
        # Should handle all strings without error
        sorted_strings = collator.sort(self.test_strings)
        self.assertEqual(len(sorted_strings), len(self.test_strings))
    
    def test_transliteration(self):
        """Test transliteration safety."""
        trans = uicu.Transliterator('Any-Latin')
        
        for text in self.test_strings:
            # Should not raise exceptions
            result = trans.transliterate(text)
            self.assertIsInstance(result, str)
```

### Locale Coverage Testing

```python
def test_locale_coverage():
    """Test with multiple locales."""
    test_locales = [
        'en-US',  # English (US)
        'en-GB',  # English (UK)
        'de-DE',  # German
        'fr-FR',  # French
        'es-ES',  # Spanish
        'it-IT',  # Italian
        'pt-BR',  # Portuguese (Brazil)
        'ru-RU',  # Russian
        'zh-CN',  # Chinese (Simplified)
        'zh-TW',  # Chinese (Traditional)
        'ja-JP',  # Japanese
        'ko-KR',  # Korean
        'ar-SA',  # Arabic
        'he-IL',  # Hebrew
        'th-TH',  # Thai
        'vi-VN',  # Vietnamese
    ]
    
    test_data = ['Apple', 'Banana', 'Cherry', '123', 'École', '北京']
    
    for locale_id in test_locales:
        try:
            # Test locale creation
            locale = uicu.Locale(locale_id)
            
            # Test collation
            collator = locale.get_collator()
            sorted_data = collator.sort(test_data)
            
            # Test formatting
            formatter = locale.get_datetime_formatter()
            formatted = formatter.format(datetime.now())
            
            print(f"✓ {locale_id}: {locale.display_name}")
        except Exception as e:
            print(f"✗ {locale_id}: {e}")
```

## Security Considerations

### Input Sanitization

```python
def sanitize_unicode_input(text, max_length=1000):
    """Sanitize Unicode input for security."""
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    
    # Length check
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove dangerous characters
    dangerous_chars = [
        '\x00',  # Null byte
        '\ufeff',  # BOM
        '\u200b',  # Zero-width space
        '\u200c',  # Zero-width non-joiner
        '\u200d',  # Zero-width joiner
        '\u2028',  # Line separator
        '\u2029',  # Paragraph separator
    ]
    
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Normalize
    trans = uicu.Transliterator('NFC')
    text = trans.transliterate(text)
    
    return text

# Example
user_input = "Hello\x00World\u200bTest"
clean = sanitize_unicode_input(user_input)
print(f"Original: {user_input!r}")
print(f"Cleaned: {clean!r}")
```

### Preventing Homograph Attacks

```python
def detect_homographs(text, whitelist_scripts=None):
    """Detect potential homograph attacks."""
    if whitelist_scripts is None:
        whitelist_scripts = {'Latn', 'Zyyy'}  # Latin + Common
    
    # Check scripts used
    scripts = set()
    for char in text:
        script = uicu.script(char)
        if script not in ('Zyyy', 'Zinh', 'Zzzz'):  # Not common/inherited
            scripts.add(script)
    
    # Mixed scripts could indicate homograph attack
    suspicious = scripts - whitelist_scripts
    
    if suspicious:
        return {
            'suspicious': True,
            'scripts': list(scripts),
            'unexpected': list(suspicious)
        }
    
    return {'suspicious': False, 'scripts': list(scripts)}

# Test
domains = [
    "google.com",      # Safe
    "gооgle.com",      # Cyrillic 'o'
    "аррӏе.com",       # Cyrillic characters
    "paypal.com",      # Safe
    "pаypal.com",      # Cyrillic 'a'
]

for domain in domains:
    result = detect_homographs(domain)
    status = "⚠️ SUSPICIOUS" if result['suspicious'] else "✓ Safe"
    print(f"{domain}: {status}")
    if result['suspicious']:
        print(f"  Scripts: {result['scripts']}")
        print(f"  Unexpected: {result['unexpected']}")
```

## Common Pitfalls

### 1. String Length vs. Character Count

```python
# ❌ Wrong
text = "café"
char_count = len(text)  # Might be 4 or 5!

# ✅ Correct
grapheme_count = len(list(uicu.graphemes(text)))  # Always 4
```

### 2. Case-Insensitive Comparison

```python
# ❌ Wrong: Simple lowercase
def bad_case_insensitive_compare(a, b):
    return a.lower() == b.lower()  # Fails for Turkish İ/i

# ✅ Correct: Use collator
def good_case_insensitive_compare(a, b, locale='en-US'):
    collator = uicu.Collator(locale, strength='primary')
    return collator.compare(a, b) == 0
```

### 3. Assuming ASCII

```python
# ❌ Wrong: ASCII assumptions
def bad_is_letter(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

# ✅ Correct: Unicode-aware
def good_is_letter(char):
    return uicu.category(char).startswith('L')
```

### 4. Hardcoded Locale Formats

```python
# ❌ Wrong: Hardcoded format
def bad_format_date(date):
    return f"{date.month}/{date.day}/{date.year}"  # US-centric

# ✅ Correct: Locale-aware
def good_format_date(date, locale='en-US'):
    formatter = uicu.DateTimeFormatter(locale, date_style='medium')
    return formatter.format(date)
```

## Summary

Key takeaways for using UICU effectively:

1. **Performance**: Reuse objects, batch operations, use pools
2. **Error Handling**: Graceful degradation, validate input
3. **Internationalization**: Respect user preferences, test globally
4. **Security**: Sanitize input, prevent homograph attacks
5. **Testing**: Use diverse data, test edge cases
6. **Memory**: Clean up properly, use lazy loading
7. **Avoid Pitfalls**: Use Unicode-aware operations

Following these practices will help you build robust, performant, and truly international applications with UICU.