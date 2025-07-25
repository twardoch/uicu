# uicu.collate

Locale-aware text collation and sorting.

This module provides culture-aware string comparison and sorting with customizable strength levels, numeric sorting, and case-first options.

## Classes

### `Collator`

::: uicu.collate.Collator

## Functions

### `compare`

::: uicu.collate.compare

### `sort`

::: uicu.collate.sort

## Examples

### Basic Sorting

```python
from uicu import Collator, sort

# Quick sort with default locale
sorted_list = sort(['banana', 'apple', 'cherry'])
print(sorted_list)  # ['apple', 'banana', 'cherry']

# Sort with specific locale
sorted_german = sort(['Müller', 'Mueller', 'Mahler'], 'de-DE')
print(sorted_german)  # German-specific ordering
```

### Using Collator Objects

```python
# Create reusable collator
collator = Collator('en-US')

# Sort multiple lists
list1 = ['zebra', 'apple', 'banana']
list2 = ['John', 'jane', 'JAMES']

sorted1 = collator.sort(list1)
sorted2 = collator.sort(list2)

# Compare strings
result = collator.compare('café', 'cafe')
print(result)  # 1 (café > cafe)
```

### Collation Strength

```python
# Primary strength - ignores case and accents
primary = Collator('en-US', strength='primary')
print(primary.compare('café', 'CAFE'))  # 0 (equal)

# Secondary strength - considers accents, ignores case
secondary = Collator('en-US', strength='secondary')
print(secondary.compare('café', 'cafe'))  # 1 (café > cafe)
print(secondary.compare('café', 'CAFÉ'))  # 0 (equal)

# Tertiary strength (default) - considers case
tertiary = Collator('en-US', strength='tertiary')
print(tertiary.compare('café', 'Café'))  # 1 (café > Café)

# Quaternary strength - considers punctuation
quaternary = Collator('en-US', strength='quaternary')
print(quaternary.compare('hello', 'hello.'))  # -1
```

### Numeric Sorting

```python
# Without numeric sorting
regular = Collator('en-US')
items = ['item2', 'item10', 'item1']
print(regular.sort(items))  # ['item1', 'item10', 'item2']

# With numeric sorting
numeric = Collator('en-US', numeric=True)
print(numeric.sort(items))  # ['item1', 'item2', 'item10']

# Works with complex patterns
files = ['v1.2.10', 'v1.2.2', 'v1.10.1']
print(numeric.sort(files))  # Natural version ordering
```

### Case-First Options

```python
# Default behavior
default = Collator('en-US')
words = ['apple', 'Apple', 'APPLE']
print(default.sort(words))

# Uppercase first
upper_first = Collator('en-US', case_first='upper')
print(upper_first.sort(words))  # ['APPLE', 'Apple', 'apple']

# Lowercase first
lower_first = Collator('en-US', case_first='lower')
print(lower_first.sort(words))  # ['apple', 'Apple', 'APPLE']
```

### Language-Specific Collation

```python
# Swedish places å, ä, ö at the end
swedish = Collator('sv-SE')
swedish_words = ['öl', 'ärlig', 'äpple', 'zoo', 'åka']
print(swedish.sort(swedish_words))

# Spanish traditional vs. modern
traditional = Collator('es-ES-u-co-trad')  # ch, ll as single letters
modern = Collator('es-ES')  # Standard ordering

# Chinese pronunciation vs. stroke order
pinyin = Collator('zh-CN')  # Default: pinyin ordering
stroke = Collator('zh-CN-u-co-stroke')  # Stroke order
```

### Sort Keys

```python
# Get sort keys for efficient sorting
collator = Collator('en-US')

# Generate sort keys
words = ['apple', 'Ärger', 'zebra']
keyed_words = [(word, collator.get_sort_key(word)) for word in words]

# Sort by keys
keyed_words.sort(key=lambda x: x[1])
sorted_words = [word for word, key in keyed_words]
print(sorted_words)

# Sort keys are useful for database storage
word = 'café'
sort_key = collator.get_sort_key(word)
print(f"Sort key for '{word}': {sort_key.hex()}")
```

## Advanced Usage

### Custom Comparison Function

```python
def create_comparator(locale='en-US', **options):
    """Create a comparison function for use with Python's sorted()."""
    collator = Collator(locale, **options)
    
    class Comparator:
        def __init__(self, obj):
            self.obj = obj
        
        def __lt__(self, other):
            return collator.compare(self.obj, other.obj) < 0
        
        def __gt__(self, other):
            return collator.compare(self.obj, other.obj) > 0
        
        def __eq__(self, other):
            return collator.compare(self.obj, other.obj) == 0
        
        def __le__(self, other):
            return collator.compare(self.obj, other.obj) <= 0
        
        def __ge__(self, other):
            return collator.compare(self.obj, other.obj) >= 0
    
    return Comparator

# Usage with Python's sorted()
Comparator = create_comparator('de-DE')
names = ['Müller', 'Mueller', 'Muller']
sorted_names = sorted(names, key=Comparator)
print(sorted_names)
```

### Multi-Level Sorting

```python
class MultiLevelCollator:
    """Sort by multiple fields with locale awareness."""
    
    def __init__(self, locale='en-US'):
        self.collator = Collator(locale)
    
    def sort_by_fields(self, items, *fields):
        """Sort items by multiple fields.
        
        Args:
            items: List of objects (dicts or objects with attributes)
            fields: Field names or accessor functions
        """
        # Sort by fields in reverse order (stable sort)
        result = list(items)
        
        for field in reversed(fields):
            if callable(field):
                key_func = field
            elif isinstance(result[0], dict):
                key_func = lambda x: x.get(field, '')
            else:
                key_func = lambda x: getattr(x, field, '')
            
            # Sort using collator
            result = sorted(result, 
                          key=lambda x: self.collator.get_sort_key(str(key_func(x))))
        
        return result

# Example
people = [
    {'first': 'José', 'last': 'García'},
    {'first': 'Jose', 'last': 'Garcia'},
    {'first': 'María', 'last': 'García'},
    {'first': 'Ana', 'last': 'Gárcia'},
]

collator = MultiLevelCollator('es-ES')
sorted_people = collator.sort_by_fields(people, 'last', 'first')
for person in sorted_people:
    print(f"{person['last']}, {person['first']}")
```

### Case-Insensitive Dictionary

```python
class CaseInsensitiveDict:
    """Dictionary with locale-aware case-insensitive keys."""
    
    def __init__(self, locale='en-US', initial=None):
        self.collator = Collator(locale, strength='primary')
        self._items = {}
        
        if initial:
            self.update(initial)
    
    def _get_key(self, key):
        """Get normalized key using sort key."""
        return self.collator.get_sort_key(key)
    
    def __setitem__(self, key, value):
        norm_key = self._get_key(key)
        self._items[norm_key] = (key, value)
    
    def __getitem__(self, key):
        norm_key = self._get_key(key)
        if norm_key in self._items:
            return self._items[norm_key][1]
        raise KeyError(key)
    
    def __contains__(self, key):
        return self._get_key(key) in self._items
    
    def items(self):
        """Return items with original keys."""
        return [(k, v) for k, v in self._items.values()]

# Usage
d = CaseInsensitiveDict('en-US')
d['Hello'] = 'world'
d['café'] = 'coffee'

print(d['hello'])  # 'world'
print(d['CAFÉ'])   # 'coffee'
print('CaFé' in d)  # True
```

## Performance Optimization

### Batch Sorting

```python
# For sorting many lists with same configuration
class BatchSorter:
    def __init__(self, locale='en-US', **options):
        self.collator = Collator(locale, **options)
    
    def sort_many(self, lists):
        """Efficiently sort multiple lists."""
        return [self.collator.sort(lst) for lst in lists]

# Usage
sorter = BatchSorter('en-US', numeric=True)
lists = [
    ['file10', 'file2', 'file1'],
    ['v1.10', 'v1.2', 'v1.9'],
    ['item99', 'item100', 'item9']
]
sorted_lists = sorter.sort_many(lists)
```

### Pre-computed Sort Keys

```python
class SortKeyCache:
    """Cache sort keys for repeated sorting."""
    
    def __init__(self, locale='en-US', **options):
        self.collator = Collator(locale, **options)
        self._cache = {}
    
    def get_sort_key(self, text):
        if text not in self._cache:
            self._cache[text] = self.collator.get_sort_key(text)
        return self._cache[text]
    
    def sort_with_cache(self, items):
        """Sort using cached keys."""
        return sorted(items, key=self.get_sort_key)

# Useful for sorting same strings multiple times
cache = SortKeyCache('en-US')
for _ in range(100):
    sorted_items = cache.sort_with_cache(large_list)
```

## Error Handling

```python
# Handle invalid locales
try:
    collator = Collator('invalid-locale')
except Exception as e:
    print(f"Error: {e}")
    collator = Collator('en-US')  # Fallback

# Safe comparison with error handling
def safe_compare(a, b, locale='en-US'):
    try:
        return compare(a, b, locale)
    except Exception:
        # Fallback to simple comparison
        return (a > b) - (a < b)
```

## Thread Safety

Collator objects are thread-safe for read operations (compare, sort, get_sort_key). Do not modify collator properties from multiple threads.

## See Also

- [Text Collation Guide](../guide/text-collation.md) - Detailed usage guide
- [`uicu.locale`](locale.md) - Locale management
- [Examples](../examples/multilingual-sorting.md) - Real-world sorting examples