---
# this_file: src_docs/md/guide/best-practices.md
title: Best Practices
description: Guidelines for effective UICU usage
---

# Best Practices

This chapter provides guidelines and best practices for effective use of UICU in production applications.

## Text Normalization

Always normalize text input for consistent processing:

```python
import uicu

def normalize_user_input(text):
    """Normalize user input for consistent processing"""
    # Normalize to NFC form
    normalized = uicu.normalize(text, 'NFC')
    # Trim whitespace
    return normalized.strip()

# Example usage
user_inputs = [
    "café",           # é as single character
    "cafe\u0301",     # e + combining accent
    "  hello  ",      # with whitespace
]

for text in user_inputs:
    normalized = normalize_user_input(text)
    print(f"'{text}' → '{normalized}'")
```

## Locale Selection

Choose appropriate locales based on user preferences:

```python
def select_best_locale(user_locales, supported_locales):
    """Select best matching locale from supported options"""
    for user_locale in user_locales:
        # Try exact match
        if user_locale in supported_locales:
            return user_locale
        
        # Try language match
        user_lang = uicu.Locale(user_locale).language
        for supported in supported_locales:
            if uicu.Locale(supported).language == user_lang:
                return supported
    
    # Fallback to English
    return 'en-US'
```

## Performance Optimization

Cache expensive objects for better performance:

```python
import functools

@functools.lru_cache(maxsize=128)
def get_collator(locale_id, strength='tertiary'):
    """Get cached collator instance"""
    collator = uicu.Collator(locale_id)
    collator.set_strength(strength)
    return collator

@functools.lru_cache(maxsize=128) 
def get_date_formatter(locale_id, style='medium'):
    """Get cached date formatter"""
    locale = uicu.Locale(locale_id)
    return locale.get_date_formatter(style=style)
```

## Error Handling

Handle Unicode errors gracefully:

```python
def safe_char_analysis(text):
    """Safely analyze characters with error handling"""
    results = []
    
    for char_str in text:
        try:
            char = uicu.Char(char_str)
            results.append({
                'char': char_str,
                'name': char.name,
                'category': char.category,
                'script': char.script,
            })
        except Exception as e:
            results.append({
                'char': char_str,
                'error': str(e),
            })
    
    return results
```

## Text Comparison

Use appropriate comparison methods:

```python
def smart_text_compare(text1, text2, locale='en-US', case_sensitive=True):
    """Smart text comparison with proper Unicode handling"""
    # Normalize both texts
    text1 = uicu.normalize(text1, 'NFC')
    text2 = uicu.normalize(text2, 'NFC')
    
    # Create collator
    collator = uicu.Collator(locale)
    
    if not case_sensitive:
        collator.set_strength('secondary')  # Ignore case
    
    return collator.compare(text1, text2) == 0
```

## Input Validation

Validate text input properly:

```python
def validate_text_input(text, max_length=1000, allow_control_chars=False):
    """Validate user text input"""
    if not text:
        return False, "Empty input"
    
    if len(text) > max_length:
        return False, f"Text too long (max {max_length})"
    
    # Check for problematic characters
    for char_str in text:
        char = uicu.Char(char_str)
        
        # Check for control characters (except whitespace)
        if char.category.startswith('C') and not char.is_whitespace:
            if not allow_control_chars:
                return False, f"Control character not allowed: {char.name}"
    
    return True, "Valid input"
```

## Memory Management

Monitor memory usage with large text processing:

```python
import gc

def process_large_text_efficiently(text, chunk_size=10000):
    """Process large text in chunks to manage memory"""
    results = []
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        
        # Process chunk
        chunk_results = []
        for char_str in chunk:
            char = uicu.Char(char_str)
            chunk_results.append({
                'char': char_str,
                'category': char.category,
                'script': char.script,
            })
        
        results.extend(chunk_results)
        
        # Periodic garbage collection
        if i % (chunk_size * 10) == 0:
            gc.collect()
    
    return results
```

Ready to explore the API reference? See [API Documentation](../api/index.md) →