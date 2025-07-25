# uicu.char

Unicode character property analysis module.

This module provides comprehensive Unicode character information by combining data from PyICU and fontTools.unicodedata.

## Classes

### `Char`

::: uicu.char.Char

## Functions

### `name`

::: uicu.char.name

### `category`

::: uicu.char.category

### `block`

::: uicu.char.block

### `script`

::: uicu.char.script

### `script_name`

::: uicu.char.script_name

### `script_extensions`

::: uicu.char.script_extensions

### `script_direction`

::: uicu.char.script_direction

### `bidirectional`

::: uicu.char.bidirectional

### `bidirectional_name`

::: uicu.char.bidirectional_name

### `combining`

::: uicu.char.combining

### `mirrored`

::: uicu.char.mirrored

### `decimal`

::: uicu.char.decimal

### `digit`

::: uicu.char.digit

### `numeric`

::: uicu.char.numeric

## Constants

### `HAS_FONTTOOLS`

Boolean indicating whether fontTools.unicodedata is available for enhanced Unicode data.

```python
if uicu.char.HAS_FONTTOOLS:
    # Use enhanced features
    script_extensions = uicu.script_extensions('a')
else:
    # Fallback behavior
    script_extensions = [uicu.script('a')]
```

## Examples

### Basic Character Analysis

```python
from uicu import Char

# Analyze a character
char = Char('€')
print(f"Character: {char.value}")
print(f"Name: {char.name}")
print(f"Category: {char.category} ({char.category_name})")
print(f"Block: {char.block}")
print(f"Script: {char.script}")
```

### Working with Complex Characters

```python
# Emoji and special characters
emoji = Char('🎉')
print(f"Emoji name: {emoji.name}")
print(f"Category: {emoji.category}")

# Combining characters
combining = Char('\u0301')  # Combining acute accent
print(f"Combining class: {combining.combining}")
print(f"Name: {combining.name}")
```

### Numeric Properties

```python
# Check numeric values
chars = ['5', '५', 'Ⅴ', '½']
for c in chars:
    char = Char(c)
    print(f"{c}: decimal={char.decimal}, digit={char.digit}, numeric={char.numeric}")
```

### Script Analysis

```python
# Analyze scripts in text
def analyze_scripts(text):
    scripts = {}
    for ch in text:
        script = uicu.script(ch)
        if script not in scripts:
            scripts[script] = []
        scripts[script].append(ch)
    
    for script, chars in scripts.items():
        script_name = uicu.script_name(script)
        print(f"{script} ({script_name}): {''.join(chars)}")

analyze_scripts("Hello мир 世界")
```

### Bidirectional Text

```python
# Check text directionality
texts = ['Hello', 'مرحبا', 'שלום', 'سلام']
for text in texts:
    char = Char(text[0])
    print(f"{text}: {char.bidirectional} ({char.bidirectional_name})")
```

## Performance Considerations

1. **Object Creation**: Creating `Char` objects has some overhead. For bulk operations, use the module-level functions.

2. **Caching**: Character properties are computed on access and not cached. Store results if you need them multiple times.

3. **fontTools Integration**: When fontTools is available, some operations may be slower but provide more accurate/complete data.

## Error Handling

The `Char` class validates input on creation:

```python
try:
    char = Char('ab')  # Error: multiple characters
except uicu.UICUError as e:
    print(f"Error: {e}")

try:
    char = Char('')  # Error: empty string
except uicu.UICUError as e:
    print(f"Error: {e}")
```

## Limitations

1. **Single Characters Only**: The `Char` class only accepts single Unicode code points. For multi-codepoint sequences (like emoji with modifiers), analyze each code point separately.

2. **Script Detection**: The module-level `detect_script()` function (from `__init__.py`) provides basic script detection for entire strings.

3. **Property Availability**: Some properties may return `None` if the data is not available in the Unicode database.

## See Also

- [Character Properties Guide](../guide/character-properties.md) - Detailed usage guide
- [Unicode Basics](../guide/unicode-basics.md) - Understanding Unicode concepts
- [`uicu.segment`](segment.md) - For handling grapheme clusters