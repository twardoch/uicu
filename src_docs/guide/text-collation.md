# Text Collation

Text collation is the process of comparing and sorting strings according to language and cultural conventions. UICU provides powerful locale-aware collation that handles the complexities of international text sorting.

## Understanding Collation

Different languages have different sorting rules:
- **English**: A < B < C... < Z
- **Swedish**: Z < Å < Ä < Ö (at the end)
- **German**: ö sorts with o (usually)
- **Spanish**: ñ comes after n
- **Chinese**: Sorted by pronunciation or stroke count

```python
import uicu

# Create collators for different locales
collator_en = uicu.Collator('en-US')
collator_sv = uicu.Collator('sv-SE')  # Swedish

# Same letters, different order
words = ['zoo', 'älg', 'öppna', 'ara']
print(f"English: {collator_en.sort(words)}")
print(f"Swedish: {collator_sv.sort(words)}")
```

## Basic Collation

### Creating Collators

```python
# Different ways to create collators
collator1 = uicu.Collator('en-US')  # Direct creation
collator2 = uicu.Collator.create_instance('de-DE')  # Factory method

# From locale object
locale = uicu.Locale('fr-FR')
collator3 = locale.get_collator()

# With options
collator4 = uicu.Collator('en-US', strength='primary', numeric=True)
```

### Comparing Strings

```python
collator = uicu.Collator('en-US')

# Compare returns: -1 (less), 0 (equal), 1 (greater)
print(collator.compare('apple', 'banana'))  # -1
print(collator.compare('apple', 'apple'))   # 0
print(collator.compare('banana', 'apple'))  # 1

# Direct comparison function
print(uicu.compare('café', 'cafe', 'en-US'))  # 1 (café > cafe)
```

### Sorting Lists

```python
# Sort various types of data
collator = uicu.Collator('en-US')

# Simple word list
words = ['banana', 'apple', 'cherry', 'apricot']
sorted_words = collator.sort(words)
print(f"Sorted: {sorted_words}")

# Names with special characters
names = ['Müller', 'Mueller', 'Muller', 'Mühler']
sorted_names = collator.sort(names)
print(f"Names: {sorted_names}")

# Mixed case
items = ['Item', 'item', 'ITEM', 'iTem']
sorted_items = collator.sort(items)
print(f"Mixed case: {sorted_items}")
```

## Collation Strength

Strength determines how different characters are considered:

### Primary Strength
Ignores case and accents:

```python
collator = uicu.Collator('en-US', strength='primary')

# These are all equal at primary strength
print(collator.compare('cafe', 'CAFE'))  # 0
print(collator.compare('cafe', 'café'))  # 0
print(collator.compare('CAFE', 'CAFÉ'))  # 0

# But these are different
print(collator.compare('cafe', 'cage'))  # -1
```

### Secondary Strength
Considers accents but ignores case:

```python
collator = uicu.Collator('en-US', strength='secondary')

# Case doesn't matter
print(collator.compare('cafe', 'CAFE'))  # 0
print(collator.compare('café', 'CAFÉ'))  # 0

# But accents do matter
print(collator.compare('cafe', 'café'))  # -1
```

### Tertiary Strength (Default)
Considers case and accents:

```python
collator = uicu.Collator('en-US', strength='tertiary')

# Everything matters
print(collator.compare('cafe', 'Cafe'))  # 1 (lowercase > uppercase)
print(collator.compare('cafe', 'café'))  # -1
print(collator.compare('Cafe', 'Café'))  # -1
```

### Quaternary Strength
Also considers punctuation and whitespace:

```python
collator = uicu.Collator('en-US', strength='quaternary')

# Even punctuation matters
print(collator.compare('hello', 'hello'))   # 0
print(collator.compare('hello', 'hello.'))  # -1
print(collator.compare('hello world', 'helloworld'))  # -1
```

## Numeric Sorting

Enable natural sorting of numbers:

```python
# Without numeric sorting
regular_collator = uicu.Collator('en-US')
items = ['item2', 'item10', 'item1', 'item20']
print(f"Regular: {regular_collator.sort(items)}")
# Output: ['item1', 'item10', 'item2', 'item20']

# With numeric sorting
numeric_collator = uicu.Collator('en-US', numeric=True)
print(f"Numeric: {numeric_collator.sort(items)}")
# Output: ['item1', 'item2', 'item10', 'item20']

# Works with complex patterns
files = ['img_2.png', 'img_10.png', 'img_1.png', 'img_100.png']
print(f"Files: {numeric_collator.sort(files)}")
```

## Case-First Options

Control whether uppercase or lowercase sorts first:

```python
# Default behavior
default_collator = uicu.Collator('en-US')
words = ['apple', 'Apple', 'banana', 'Banana']
print(f"Default: {default_collator.sort(words)}")

# Uppercase first
upper_first = uicu.Collator('en-US', case_first='upper')
print(f"Upper first: {upper_first.sort(words)}")

# Lowercase first
lower_first = uicu.Collator('en-US', case_first='lower')
print(f"Lower first: {lower_first.sort(words)}")
```

## Language-Specific Rules

### German Collation

```python
# German phonebook vs. dictionary ordering
words = ['Müller', 'Mueller', 'Muller']

# Standard German collation
collator_de = uicu.Collator('de-DE')
print(f"Standard: {collator_de.sort(words)}")

# Phonebook collation (ü = ue)
collator_phonebook = uicu.Collator('de-DE-u-co-phonebk')
print(f"Phonebook: {collator_phonebook.sort(words)}")
```

### Chinese Collation

```python
# Chinese can be sorted by pronunciation (pinyin) or stroke count
chinese_names = ['张', '李', '王', '刘', '陈']

# Pinyin-based sorting (default for simplified Chinese)
collator_pinyin = uicu.Collator('zh-CN')
sorted_pinyin = collator_pinyin.sort(chinese_names)
print(f"Pinyin: {sorted_pinyin}")

# Stroke-based sorting
collator_stroke = uicu.Collator('zh-CN-u-co-stroke')
sorted_stroke = collator_stroke.sort(chinese_names)
print(f"Stroke: {sorted_stroke}")
```

### Japanese Collation

```python
# Japanese sorting with different scripts
japanese_words = ['さくら', 'サクラ', '桜', 'sakura', '佐倉']

collator_ja = uicu.Collator('ja-JP')
sorted_ja = collator_ja.sort(japanese_words)
print(f"Japanese: {sorted_ja}")
```

## Sort Keys

For efficient sorting of large datasets:

```python
collator = uicu.Collator('en-US')

# Generate sort keys
words = ['banana', 'apple', 'cherry']
sort_keys = [(word, collator.get_sort_key(word)) for word in words]

# Sort by keys (more efficient for large lists)
sort_keys.sort(key=lambda x: x[1])
sorted_words = [word for word, key in sort_keys]
print(f"Sorted by keys: {sorted_words}")

# Demonstrate key structure
word = 'café'
key = collator.get_sort_key(word)
print(f"Sort key for '{word}': {key.hex()}")
```

## Advanced Collation Options

### Custom Rules

```python
# Create collator with custom rules (ICU rule syntax)
# Make 'x' sort after 'z'
custom_rules = "&z < x"
collator = uicu.Collator('en-US')
# Note: Custom rules require ICU API not exposed in basic wrapper

# Alternative: Use transliteration for preprocessing
trans = uicu.Transliterator('NFD')  # Decompose accents
words = ['café', 'cake', 'cafè']

# Sort with decomposed forms
decomposed = [trans.transliterate(w) for w in words]
sorted_indices = sorted(range(len(words)), key=lambda i: decomposed[i])
sorted_words = [words[i] for i in sorted_indices]
print(f"Custom sorted: {sorted_words}")
```

### Handling Null and Empty Values

```python
def sort_with_nulls(items, collator, nulls_first=True):
    """Sort list with None values."""
    null_value = '' if nulls_first else '\uffff'
    
    def sort_key(item):
        if item is None:
            return null_value
        return item
    
    return sorted(items, key=lambda x: collator.get_sort_key(sort_key(x)))

# Example
items = ['banana', None, 'apple', '', 'cherry', None]
collator = uicu.Collator('en-US')

sorted_nulls_first = sort_with_nulls(items, collator, nulls_first=True)
sorted_nulls_last = sort_with_nulls(items, collator, nulls_first=False)

print(f"Nulls first: {sorted_nulls_first}")
print(f"Nulls last: {sorted_nulls_last}")
```

## Practical Examples

### Sorting Names

```python
class NameSorter:
    """Sort names with proper handling of particles and titles."""
    
    def __init__(self, locale='en-US'):
        self.collator = uicu.Collator(locale)
        self.titles = {'Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.'}
        self.particles = {'de', 'von', 'van', 'der', 'la', 'le'}
    
    def parse_name(self, name):
        """Parse name into sortable components."""
        parts = name.split()
        title = None
        particle = None
        
        # Extract title
        if parts and parts[0] in self.titles:
            title = parts.pop(0)
        
        # Extract particle (simplified)
        for i, part in enumerate(parts[:-1]):
            if part.lower() in self.particles:
                particle = ' '.join(parts[i:-1])
                last = parts[-1]
                first = ' '.join(parts[:i]) if i > 0 else ''
                return title, first, particle, last
        
        # No particle
        if len(parts) >= 2:
            first = ' '.join(parts[:-1])
            last = parts[-1]
        else:
            first = ''
            last = ' '.join(parts)
        
        return title, first, particle, last
    
    def sort_key(self, name):
        """Generate sort key for name."""
        title, first, particle, last = self.parse_name(name)
        
        # Sort by: last name, first name, particle, title
        if particle:
            key = f"{last}, {first} {particle}"
        else:
            key = f"{last}, {first}"
        
        return self.collator.get_sort_key(key.strip())
    
    def sort_names(self, names):
        """Sort list of names."""
        return sorted(names, key=self.sort_key)

# Example usage
sorter = NameSorter()
names = [
    'John Smith',
    'Dr. Jane Smith',
    'Pierre de La Fontaine',
    'Ludwig van Beethoven',
    'Maria von Trapp',
    'John van der Berg',
    'Ana García',
    'José García',
]

sorted_names = sorter.sort_names(names)
print("Sorted names:")
for name in sorted_names:
    print(f"  {name}")
```

### Multi-Level Sorting

```python
class MultiLevelSorter:
    """Sort by multiple criteria."""
    
    def __init__(self, locale='en-US'):
        self.collator = uicu.Collator(locale)
    
    def sort(self, items, *keys):
        """Sort by multiple keys in order."""
        # Sort by keys in reverse order (stable sort)
        result = list(items)
        for key in reversed(keys):
            result = sorted(result, 
                          key=lambda x: self.collator.get_sort_key(str(key(x))))
        return result

# Example: Sort products by category, then name
products = [
    {'name': 'Banana', 'category': 'Fruit', 'price': 0.99},
    {'name': 'Apple', 'category': 'Fruit', 'price': 1.29},
    {'name': 'Carrot', 'category': 'Vegetable', 'price': 0.79},
    {'name': 'Broccoli', 'category': 'Vegetable', 'price': 1.49},
    {'name': 'Cherry', 'category': 'Fruit', 'price': 2.99},
]

sorter = MultiLevelSorter()
sorted_products = sorter.sort(
    products,
    lambda p: p['category'],
    lambda p: p['name']
)

print("Products sorted by category, then name:")
for product in sorted_products:
    print(f"  {product['category']:10} {product['name']:10} ${product['price']:.2f}")
```

### Case-Insensitive Dictionary

```python
class CaseInsensitiveDict:
    """Dictionary with locale-aware case-insensitive keys."""
    
    def __init__(self, locale='en-US', strength='primary'):
        self.collator = uicu.Collator(locale, strength=strength)
        self._data = {}
    
    def _get_key(self, key):
        """Get normalized key."""
        return self.collator.get_sort_key(key)
    
    def __setitem__(self, key, value):
        self._data[self._get_key(key)] = (key, value)
    
    def __getitem__(self, key):
        return self._data[self._get_key(key)][1]
    
    def __contains__(self, key):
        return self._get_key(key) in self._data
    
    def items(self):
        """Return items with original keys."""
        return [(k, v) for k, v in self._data.values()]

# Example usage
ci_dict = CaseInsensitiveDict()
ci_dict['Hello'] = 'world'
ci_dict['café'] = 'coffee'

print(ci_dict['hello'])  # Works!
print(ci_dict['HELLO'])  # Also works!
print(ci_dict['Café'])   # Works with accents!

print("\nAll items:")
for key, value in ci_dict.items():
    print(f"  {key} -> {value}")
```

## Performance Tips

### 1. Reuse Collators

```python
# Bad: Creating new collator each time
def slow_sort(items, locale='en-US'):
    return uicu.Collator(locale).sort(items)

# Good: Reuse collator
class FastSorter:
    def __init__(self, locale='en-US'):
        self.collator = uicu.Collator(locale)
    
    def sort(self, items):
        return self.collator.sort(items)

# Performance comparison
import time
items = ['item'] * 1000

# Slow method
start = time.time()
for _ in range(100):
    slow_sort(items)
slow_time = time.time() - start

# Fast method
sorter = FastSorter()
start = time.time()
for _ in range(100):
    sorter.sort(items)
fast_time = time.time() - start

print(f"Slow: {slow_time:.3f}s")
print(f"Fast: {fast_time:.3f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

### 2. Use Sort Keys for Large Datasets

```python
# For large datasets, pre-compute sort keys
def efficient_sort(items, collator):
    # Pre-compute all sort keys
    keyed_items = [(item, collator.get_sort_key(item)) for item in items]
    
    # Sort by pre-computed keys
    keyed_items.sort(key=lambda x: x[1])
    
    # Extract sorted items
    return [item for item, key in keyed_items]

# This is especially efficient when sorting the same data multiple times
```

### 3. Choose Appropriate Strength

```python
# Use the minimum strength needed
# Primary is fastest, quaternary is slowest

# For case-insensitive sorting, use primary
username_collator = uicu.Collator('en-US', strength='primary')

# For general text, use tertiary (default)
text_collator = uicu.Collator('en-US')

# Only use quaternary when punctuation matters
strict_collator = uicu.Collator('en-US', strength='quaternary')
```

## Common Patterns

### Sort with Custom Order

```python
def sort_with_priority(items, collator, priority_items):
    """Sort items with some having priority."""
    priority_set = set(priority_items)
    
    def sort_key(item):
        # Priority items sort first
        priority = 0 if item in priority_set else 1
        return (priority, collator.get_sort_key(item))
    
    return sorted(items, key=sort_key)

# Example
items = ['Apple', 'Banana', 'VIP Item', 'Cherry', 'Special']
priority = ['VIP Item', 'Special']
collator = uicu.Collator('en-US')

sorted_items = sort_with_priority(items, collator, priority)
print(f"With priority: {sorted_items}")
```

### Locale-Aware Search

```python
def locale_search(haystack, needle, locale='en-US', strength='primary'):
    """Search with locale-aware comparison."""
    collator = uicu.Collator(locale, strength=strength)
    needle_key = collator.get_sort_key(needle)
    
    matches = []
    for item in haystack:
        if collator.get_sort_key(item) == needle_key:
            matches.append(item)
    
    return matches

# Example
items = ['Café', 'cafe', 'CAFE', 'cafè', 'coffee']
results = locale_search(items, 'cafe')
print(f"Matches for 'cafe': {results}")
```

## Next Steps

- Explore [Text Segmentation](text-segmentation.md) for breaking text
- Learn about [Transliteration](transliteration.md) for text transformation
- Master [Date/Time Formatting](date-time-formatting.md) with locales