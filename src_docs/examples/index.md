# Examples

This section provides practical, real-world examples of using UICU in various applications.

## Example Categories

<div class="grid cards" markdown>

-   :material-format-letter-case:{ .lg .middle } **[Character Analysis](character-analysis.md)**

    ---

    Explore Unicode characters, analyze text properties, and handle complex scripts

    [:octicons-arrow-right-24: View examples](character-analysis.md)

-   :material-sort-alphabetical-ascending:{ .lg .middle } **[Multilingual Sorting](multilingual-sorting.md)**

    ---

    Sort names, products, and data according to different cultural conventions

    [:octicons-arrow-right-24: View examples](multilingual-sorting.md)

-   :material-text-box-outline:{ .lg .middle } **[Text Processing](text-processing.md)**

    ---

    Segment text, handle word boundaries, and process multilingual content

    [:octicons-arrow-right-24: View examples](text-processing.md)

-   :material-translate:{ .lg .middle } **[Script Conversion](script-conversion.md)**

    ---

    Convert between writing systems, romanize text, and normalize content

    [:octicons-arrow-right-24: View examples](script-conversion.md)

-   :material-earth:{ .lg .middle } **[Locale-Aware Apps](locale-aware-apps.md)**

    ---

    Build applications that adapt to user language and regional preferences

    [:octicons-arrow-right-24: View examples](locale-aware-apps.md)

</div>

## Quick Examples

### Unicode Character Explorer

```python
import uicu

def explore_character(char):
    """Display comprehensive information about a character."""
    try:
        c = uicu.Char(char)
        print(f"Character: {c.value}")
        print(f"Name: {c.name}")
        print(f"Category: {c.category} ({c.category_name})")
        print(f"Script: {c.script} ({c.script_name})")
        print(f"Block: {c.block}")
        print(f"Bidirectional: {c.bidirectional}")
        
        if c.numeric is not None:
            print(f"Numeric value: {c.numeric}")
    except uicu.UICUError as e:
        print(f"Error: {e}")

# Try it with various characters
explore_character('A')
explore_character('中')
explore_character('🎉')
```

### Smart Text Truncation

```python
import uicu

def smart_truncate(text, max_length, locale='en-US'):
    """Truncate text at word boundaries."""
    if len(text) <= max_length:
        return text
    
    # Find word boundaries
    words = list(uicu.words(text, locale=locale))
    if not words:
        return text[:max_length] + "..."
    
    result = ""
    for word in words:
        if len(result) + len(word) + 3 > max_length:  # +3 for "..."
            break
        result += word + " "
    
    return result.strip() + "..."

# Examples
print(smart_truncate("This is a very long sentence that needs truncation", 20))
print(smart_truncate("Short text", 20))
```

### International Name Formatter

```python
import uicu

class NameFormatter:
    """Format names according to cultural conventions."""
    
    def __init__(self, locale='en-US'):
        self.locale = uicu.Locale(locale)
        self.collator = self.locale.get_collator()
    
    def format_name(self, first, last, title=None):
        """Format name based on locale conventions."""
        lang = self.locale.language
        
        if lang in ['ja', 'zh', 'ko']:  # East Asian
            name = f"{last}{first}"
            if title:
                name = f"{title} {name}"
        elif lang in ['hu']:  # Hungarian
            name = f"{last} {first}"
            if title:
                name = f"{title} {name}"
        else:  # Western style
            name = f"{first} {last}"
            if title:
                name = f"{title} {name}"
        
        return name
    
    def sort_names(self, names):
        """Sort names according to locale rules."""
        return self.collator.sort(names)

# Usage
formatter = NameFormatter('ja-JP')
print(formatter.format_name('太郎', '山田', '様'))

formatter_us = NameFormatter('en-US')
print(formatter_us.format_name('John', 'Smith', 'Dr.'))
```

## Common Patterns

### 1. Text Analysis Pipeline

```python
import uicu

def analyze_text(text, locale='en-US'):
    """Complete text analysis pipeline."""
    results = {
        'locale': locale,
        'length': len(text),
        'graphemes': len(list(uicu.graphemes(text))),
        'words': list(uicu.words(text, locale=locale)),
        'sentences': list(uicu.sentences(text, locale=locale)),
        'scripts': set(),
        'categories': {}
    }
    
    # Analyze character properties
    for char in text:
        script = uicu.script(char)
        if script not in ('Zyyy', 'Zinh'):
            results['scripts'].add(script)
        
        category = uicu.category(char)
        results['categories'][category] = results['categories'].get(category, 0) + 1
    
    results['scripts'] = list(results['scripts'])
    results['primary_script'] = uicu.detect_script(text)
    
    return results

# Example
text = "Hello, 世界! How are you? 🌍"
analysis = analyze_text(text)
print(f"Text: '{text}'")
print(f"Words: {len(analysis['words'])}")
print(f"Scripts: {analysis['scripts']}")
print(f"Primary script: {analysis['primary_script']}")
```

### 2. Locale-Aware Search

```python
import uicu

class LocaleAwareSearch:
    """Search with locale-specific matching."""
    
    def __init__(self, locale='en-US'):
        self.collator = uicu.Collator(locale, strength='primary')
    
    def search(self, items, query):
        """Find items matching query (case/accent insensitive)."""
        matches = []
        query_key = self.collator.get_sort_key(query)
        
        for item in items:
            if self.collator.get_sort_key(item) == query_key:
                matches.append(item)
        
        return matches
    
    def fuzzy_search(self, items, query):
        """Find items containing query."""
        matches = []
        for item in items:
            words = list(uicu.words(item))
            query_words = list(uicu.words(query))
            
            # Check if all query words are in item
            if all(any(self.collator.compare(qw, iw) == 0 for iw in words) 
                   for qw in query_words):
                matches.append(item)
        
        return matches

# Usage
searcher = LocaleAwareSearch('en-US')
items = ['Café Luna', 'cafe luna', 'CAFÉ LUNA', 'Restaurant Café']
print(searcher.search(items, 'cafe luna'))  # Finds all variations
```

### 3. Data Validation

```python
import uicu

class UnicodeValidator:
    """Validate Unicode text for various purposes."""
    
    @staticmethod
    def is_single_script(text, allowed_scripts=None):
        """Check if text uses only allowed scripts."""
        scripts = set()
        for char in text:
            script = uicu.script(char)
            if script not in ('Zyyy', 'Zinh', 'Zzzz'):
                scripts.add(script)
        
        if allowed_scripts:
            return scripts.issubset(allowed_scripts)
        return len(scripts) <= 1
    
    @staticmethod
    def has_rtl_text(text):
        """Check if text contains RTL characters."""
        for char in text:
            bidi = uicu.bidirectional(char)
            if bidi in ('R', 'AL'):
                return True
        return False
    
    @staticmethod
    def normalize_whitespace(text):
        """Normalize various Unicode spaces."""
        trans = uicu.Transliterator('[:Zs:] > \' \'')
        return trans.transliterate(text)

# Usage
validator = UnicodeValidator()
print(validator.is_single_script('Hello'))  # True
print(validator.is_single_script('Hello مرحبا'))  # False
print(validator.has_rtl_text('Hello مرحبا'))  # True
```

## Running the Examples

All examples in this section are self-contained and can be run directly:

```bash
# Save any example to a file
python example.py

# Or run interactively
python -i example.py
```

## Contributing Examples

Have a great UICU example? We'd love to include it! Please:

1. Ensure the example is self-contained
2. Include clear comments explaining the purpose
3. Test with multiple locales/scripts where relevant
4. Submit via GitHub pull request

## Next Steps

- Explore specific example categories for detailed use cases
- Check the [User Guide](../guide/index.md) for conceptual understanding
- See the [API Reference](../api/index.md) for complete documentation