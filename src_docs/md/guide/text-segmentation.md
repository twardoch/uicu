---
# this_file: src_docs/md/guide/text-segmentation.md
title: Text Segmentation
description: Smart text breaking and boundary detection
---

# Text Segmentation

Proper text segmentation is crucial for text processing. UICU follows Unicode Text Segmentation standards for breaking text into graphemes, words, sentences, and lines.

## Grapheme Segmentation

User-perceived characters (graphemes) may span multiple Unicode code points:

```python
import uicu

# Complex graphemes
examples = [
    "é",                    # Single character
    "e\u0301",             # e + combining acute
    "👨‍👩‍👧‍👦",              # Family emoji sequence
    "🇺🇸",                   # Flag emoji
    "नमस्ते",                # Devanagari text
]

for text in examples:
    graphemes = list(uicu.graphemes(text))
    print(f"'{text}' → {len(graphemes)} graphemes: {graphemes}")
```

## Word Segmentation

Break text into words following Unicode rules:

```python
# Multilingual word segmentation
texts = [
    "Hello, world! 123",
    "こんにちは世界",          # Japanese (no spaces)
    "مرحبا بالعالم",           # Arabic
    "Price: $100.50",
]

for text in texts:
    words = list(uicu.words(text))
    word_list = [w.text for w in words if w.is_word]
    print(f"'{text}' → {word_list}")
```

## Sentence Segmentation

Intelligent sentence boundary detection:

```python
# Complex sentence boundaries
text = """
Dr. Smith went to the U.S.A. He met Prof. Johnson. 
They discussed AI research. What an exciting day!
"""

sentences = list(uicu.sentences(text.strip()))
for i, sentence in enumerate(sentences, 1):
    print(f"{i}: {sentence.text.strip()}")
```

## Line Breaking

Determine appropriate line break opportunities:

```python
def wrap_text(text, width=20):
    """Simple text wrapping using line break opportunities"""
    breaks = list(uicu.line_breaks(text))
    lines = []
    current_line = ""
    
    for i, char in enumerate(text):
        current_line += char
        
        # Check if we can break here and line is long enough
        if i in breaks and len(current_line) >= width:
            lines.append(current_line.strip())
            current_line = ""
    
    if current_line.strip():
        lines.append(current_line.strip())
    
    return lines

# Wrap long text
long_text = "This is a very long sentence that needs to be wrapped properly according to Unicode line breaking rules."
wrapped = wrap_text(long_text)
for line in wrapped:
    print(f"'{line}'")
```

Continue to [Transliteration](transliteration.md) →