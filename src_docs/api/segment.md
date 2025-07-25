# uicu.segment

Text boundary analysis and segmentation module.

This module provides Unicode-compliant text segmentation for graphemes, words, sentences, and line breaks.

## Classes

### `GraphemeSegmenter`

::: uicu.segment.GraphemeSegmenter

### `WordSegmenter`

::: uicu.segment.WordSegmenter

### `SentenceSegmenter`

::: uicu.segment.SentenceSegmenter

### `LineSegmenter`

::: uicu.segment.LineSegmenter

## Functions

### `graphemes`

::: uicu.segment.graphemes

### `words`

::: uicu.segment.words

### `sentences`

::: uicu.segment.sentences

### `line_breaks`

::: uicu.segment.line_breaks

### `lines`

::: uicu.segment.lines

## Examples

### Basic Segmentation

```python
from uicu import graphemes, words, sentences

# Grapheme segmentation
text = "👨‍👩‍👧‍👦 is a family"
g = list(graphemes(text))
print(f"Graphemes: {g}")  # ['👨‍👩‍👧‍👦', ' ', 'i', 's', ...]

# Word segmentation
text = "Hello, world! How are you?"
w = list(words(text))
print(f"Words: {w}")  # ['Hello', 'world', 'How', 'are', 'you']

# Sentence segmentation
text = "Dr. Smith went to N.Y.C. yesterday. He's busy!"
s = list(sentences(text))
print(f"Sentences: {s}")  # Handles abbreviations correctly
```

### Language-Specific Segmentation

```python
from uicu import WordSegmenter

# Thai word segmentation (no spaces between words)
thai_segmenter = WordSegmenter('th-TH')
thai_text = "สวัสดีครับยินดีต้อนรับ"
words = list(thai_segmenter.segment(thai_text))
print(f"Thai words: {words}")

# Chinese word segmentation
chinese_segmenter = WordSegmenter('zh-CN')
chinese_text = "我喜欢编程"
words = list(chinese_segmenter.segment(chinese_text))
print(f"Chinese words: {words}")

# Japanese mixed script
japanese_segmenter = WordSegmenter('ja-JP')
japanese_text = "私はPythonが大好きです"
words = list(japanese_segmenter.segment(japanese_text))
print(f"Japanese words: {words}")
```

### Grapheme Clusters

```python
from uicu import GraphemeSegmenter

segmenter = GraphemeSegmenter()

# Complex emoji sequences
emoji_tests = [
    "👨‍👩‍👧‍👦",  # Family
    "🏳️‍🌈",     # Rainbow flag
    "👋🏽",        # Waving hand with skin tone
    "🇺🇸🇬🇧",     # Flags
]

for text in emoji_tests:
    graphemes = list(segmenter.segment(text))
    print(f"'{text}' has {len(graphemes)} grapheme(s): {graphemes}")

# Combining characters
combining_text = "é"  # e + combining acute
graphemes = list(segmenter.segment(combining_text))
print(f"Combining: {graphemes}")
```

### Sentence Segmentation with Abbreviations

```python
from uicu import SentenceSegmenter

# Create segmenter for English
segmenter = SentenceSegmenter('en-US')

# Test with abbreviations
text = """
Dr. John Smith, Ph.D., works at I.B.M. Corp. He lives in the U.S.A. 
His email is john@example.com. He said "Hello!" Then he left.
"""

sentences = list(segmenter.segment(text.strip()))
for i, sent in enumerate(sentences, 1):
    print(f"{i}. {sent!r}")
```

### Line Breaking

```python
from uicu import line_breaks, LineSegmenter

# Find line break opportunities
text = "This is a very long sentence that might need to be wrapped."
breaks = list(line_breaks(text))
print(f"Break positions: {breaks}")

# Implement text wrapping
def wrap_text(text, width=20, locale='en-US'):
    """Wrap text at appropriate boundaries."""
    segmenter = LineSegmenter(locale)
    breaks = list(segmenter.find_breaks(text))
    
    lines = []
    start = 0
    
    for i, pos in enumerate(breaks):
        if pos - start >= width:
            # Find previous break point
            if i > 0:
                lines.append(text[start:breaks[i-1]])
                start = breaks[i-1]
    
    # Add remaining text
    if start < len(text):
        lines.append(text[start:])
    
    return lines

wrapped = wrap_text("This is a very long sentence that needs wrapping.", 20)
for line in wrapped:
    print(f"'{line}'")
```

### Reusable Segmenters

```python
from uicu import WordSegmenter, SentenceSegmenter

class TextProcessor:
    """Reusable text processor with cached segmenters."""
    
    def __init__(self, locale='en-US'):
        self.word_segmenter = WordSegmenter(locale)
        self.sentence_segmenter = SentenceSegmenter(locale)
    
    def extract_words(self, text):
        """Extract all words from text."""
        return list(self.word_segmenter.segment(text))
    
    def extract_sentences(self, text):
        """Extract all sentences from text."""
        return list(self.sentence_segmenter.segment(text))
    
    def word_count(self, text):
        """Count words in text."""
        return len(self.extract_words(text))
    
    def sentence_count(self, text):
        """Count sentences in text."""
        return len(self.extract_sentences(text))

# Use the processor
processor = TextProcessor('en-US')

text = "Hello world! This is a test. How many words and sentences?"
print(f"Words: {processor.word_count(text)}")
print(f"Sentences: {processor.sentence_count(text)}")
```

## Performance Considerations

1. **Reuse Segmenters**: Creating segmenter objects is expensive. Create once and reuse.

2. **Batch Processing**: Process multiple texts with the same segmenter for better performance.

3. **Memory Usage**: Segmenters maintain internal state. For large-scale processing, consider pooling.

4. **Locale Matters**: Different locales have different segmentation rules, especially for languages without spaces.

```python
import time

# Performance comparison
text = "Hello world! " * 1000

# Method 1: Create segmenter each time (slow)
start = time.time()
for _ in range(100):
    words = list(words(text))  # Creates new segmenter internally
slow_time = time.time() - start

# Method 2: Reuse segmenter (fast)
segmenter = WordSegmenter('en-US')
start = time.time()
for _ in range(100):
    words = list(segmenter.segment(text))
fast_time = time.time() - start

print(f"Create each time: {slow_time:.3f}s")
print(f"Reuse segmenter: {fast_time:.3f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

## Edge Cases

### Empty and Special Input

```python
# Edge cases
edge_cases = [
    "",                    # Empty string
    " ",                   # Single space
    "\n",                  # Newline
    "...",                 # Only punctuation
    "!!!",                 # Multiple punctuation
    "test",                # Single word
    "🎉",                  # Single emoji
]

for text in edge_cases:
    w = list(words(text))
    s = list(sentences(text))
    print(f"'{text}' -> words: {w}, sentences: {s}")
```

### Mixed Scripts and Languages

```python
# Mixed script handling
mixed_texts = [
    "Hello 世界",          # English + Chinese
    "Café コーヒー",       # French + Japanese
    "Привет world",       # Russian + English
    "مرحبا Hello",        # Arabic + English (RTL + LTR)
]

for text in mixed_texts:
    w = list(words(text, locale='en-US'))
    print(f"'{text}' -> {w}")
```

## Common Patterns

### Text Statistics

```python
def analyze_text(text, locale='en-US'):
    """Get comprehensive text statistics."""
    return {
        'characters': len(text),
        'graphemes': len(list(graphemes(text))),
        'words': len(list(words(text, locale=locale))),
        'sentences': len(list(sentences(text, locale=locale))),
        'lines': len(list(lines(text, locale=locale))),
    }

text = "Hello! 👋 This is a test. Multiple sentences here."
stats = analyze_text(text)
for key, value in stats.items():
    print(f"{key}: {value}")
```

### Smart Truncation

```python
def truncate_at_word(text, max_length, locale='en-US'):
    """Truncate text at word boundary."""
    if len(text) <= max_length:
        return text
    
    words_list = list(words(text, locale=locale))
    result = ""
    
    for word in words_list:
        if len(result) + len(word) + 1 <= max_length - 3:  # -3 for "..."
            result += word + " "
        else:
            break
    
    return result.strip() + "..."

# Example
long_text = "This is a very long text that needs to be truncated properly"
print(truncate_at_word(long_text, 30))
```

## See Also

- [Text Segmentation Guide](../guide/text-segmentation.md) - Detailed usage guide
- [Unicode Basics](../guide/unicode-basics.md) - Understanding text boundaries
- [`uicu.char`](char.md) - Character properties