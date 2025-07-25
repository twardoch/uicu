# Text Segmentation

Text segmentation is the process of dividing text into meaningful units like graphemes (user-perceived characters), words, sentences, and line breaks. UICU provides Unicode-compliant segmentation that handles complex scripts and languages correctly.

## Understanding Text Boundaries

Text segmentation is more complex than it appears:
- **Graphemes**: What users see as one character (emoji families, flags)
- **Words**: Language-dependent (no spaces in Chinese/Japanese)
- **Sentences**: Must handle abbreviations, numbers, and punctuation
- **Lines**: Where text can be wrapped

```python
import uicu

# Simple example showing the complexity
text = "Dr. Smith said: 'Hello!' 你好。👨‍👩‍👧‍👦"

print(f"String length: {len(text)}")  # Code points
print(f"Graphemes: {len(list(uicu.graphemes(text)))}")  # User-perceived characters
print(f"Words: {len(list(uicu.words(text)))}")
print(f"Sentences: {len(list(uicu.sentences(text)))}")
```

## Grapheme Segmentation

Graphemes are user-perceived characters, which may consist of multiple Unicode code points.

### Basic Grapheme Segmentation

```python
# Grapheme clusters vs. code points
examples = [
    "café",           # é might be one or two code points
    "👨‍👩‍👧‍👦",          # Family emoji (7 code points, 1 grapheme)
    "🏳️‍🌈",           # Rainbow flag (4 code points, 1 grapheme)
    "a\u0301",        # a + combining acute accent
    "한국어",          # Korean characters
    "🇺🇸",            # Flag (2 code points, 1 grapheme)
]

for text in examples:
    graphemes = list(uicu.graphemes(text))
    print(f"'{text}': {len(text)} code points, {len(graphemes)} graphemes")
    print(f"  Graphemes: {graphemes}")
```

### Complex Grapheme Examples

```python
# Various types of multi-codepoint graphemes
complex_graphemes = [
    # Emoji with skin tone modifiers
    ("👋", "Waving hand"),
    ("👋🏻", "Waving hand: light skin"),
    ("👋🏿", "Waving hand: dark skin"),
    
    # Emoji ZWJ sequences
    ("👨‍⚕️", "Man health worker"),
    ("👩‍💻", "Woman technologist"),
    ("🧑‍🤝‍🧑", "People holding hands"),
    
    # Regional indicator sequences (flags)
    ("🇯🇵", "Japan flag"),
    ("🇬🇧", "UK flag"),
    ("🇺🇳", "UN flag"),
    
    # Combining characters
    ("é", "Precomposed e-acute"),
    ("é", "e + combining acute"),
]

for text, desc in complex_graphemes:
    graphemes = list(uicu.graphemes(text))
    print(f"{desc}: '{text}'")
    print(f"  Code points: {len(text)}, Graphemes: {len(graphemes)}")
```

### Using GraphemeSegmenter

```python
# Create reusable segmenter for better performance
segmenter = uicu.GraphemeSegmenter()

# Process multiple texts
texts = [
    "Hello! 👋",
    "Family: 👨‍👩‍👧‍👦",
    "Flags: 🇺🇸🇬🇧🇯🇵",
    "Tête-à-tête café",
]

for text in texts:
    graphemes = list(segmenter.segment(text))
    print(f"'{text}' → {graphemes}")
```

## Word Segmentation

Word boundaries depend heavily on the language and script.

### Basic Word Segmentation

```python
# English word segmentation
text = "Hello, world! How are you doing today?"
words = list(uicu.words(text))
print(f"English words: {words}")

# Note: punctuation is not included in words
text_with_punctuation = "Well... I don't know—maybe?"
words = list(uicu.words(text_with_punctuation))
print(f"Words only: {words}")
```

### Language-Specific Word Breaking

```python
# Languages without spaces need special handling
examples = [
    ("Hello world", "en", "English"),
    ("Helloworld", "en", "English (no spaces)"),
    ("你好世界", "zh", "Chinese"),
    ("こんにちは世界", "ja", "Japanese"),
    ("สวัสดีครับ", "th", "Thai"),
    ("Привет мир", "ru", "Russian"),
]

for text, locale, lang in examples:
    words = list(uicu.words(text, locale=locale))
    print(f"{lang}: '{text}' → {words}")
```

### Complex Word Segmentation

```python
# Handle contractions, numbers, and special cases
test_cases = [
    "don't",
    "can't",
    "it's",
    "rock'n'roll",
    "U.S.A.",
    "3.14159",
    "test@example.com",
    "http://example.com",
    "C++",
    "#hashtag",
    "@mention",
]

for text in test_cases:
    words = list(uicu.words(text))
    print(f"'{text}' → {words}")
```

### Using WordSegmenter

```python
# Create locale-specific word segmenter
en_segmenter = uicu.WordSegmenter('en-US')
th_segmenter = uicu.WordSegmenter('th-TH')

# English text
en_text = "The quick brown fox jumps."
en_words = list(en_segmenter.segment(en_text))
print(f"English: {en_words}")

# Thai text (no spaces between words)
th_text = "ภาษาไทยไม่มีช่องว่าง"
th_words = list(th_segmenter.segment(th_text))
print(f"Thai: {th_words}")

# Mixed script text
mixed = "Hello สวัสดี 你好"
mixed_words = list(en_segmenter.segment(mixed))
print(f"Mixed: {mixed_words}")
```

## Sentence Segmentation

Sentence segmentation handles abbreviations, decimals, and language-specific rules.

### Basic Sentence Segmentation

```python
# Simple sentence breaking
text = "Hello world. How are you? I'm fine! Thanks."
sentences = list(uicu.sentences(text))
for i, sent in enumerate(sentences):
    print(f"Sentence {i+1}: '{sent}'")
```

### Handling Abbreviations

```python
# Sentence segmentation with abbreviations
text = """Dr. Smith went to Washington D.C. yesterday. He met with 
Prof. Johnson at 3 p.m. They discussed the U.S. economy."""

sentences = list(uicu.sentences(text))
for i, sent in enumerate(sentences):
    print(f"Sentence {i+1}: '{sent.strip()}'")
```

### Complex Sentence Cases

```python
# Various challenging cases
test_texts = [
    # Decimal numbers
    "The value is 3.14. That's the value of pi.",
    
    # Ellipsis
    "Well... I don't know... Maybe tomorrow.",
    
    # Questions and exclamations
    "Really?! That's amazing! Isn't it?",
    
    # Quotes
    'He said "Hello." Then he left.',
    
    # URLs and emails
    "Visit https://example.com. Contact us at info@example.com.",
    
    # Mixed languages
    "这是中文。This is English. C'est français.",
]

for text in test_texts:
    print(f"\nText: '{text}'")
    sentences = list(uicu.sentences(text))
    for i, sent in enumerate(sentences):
        print(f"  {i+1}: '{sent.strip()}'")
```

### Using SentenceSegmenter

```python
# Create reusable sentence segmenter
segmenter = uicu.SentenceSegmenter('en-US')

# Process a document
document = """
Natural language processing (NLP) is fascinating. It involves many 
challenges, e.g., tokenization, parsing, etc. Dr. Manning from 
Stanford Univ. wrote about it extensively.

Did you know? The field has grown tremendously! Machine learning 
models like GPT-3 have 175B parameters... That's huge!
"""

sentences = list(segmenter.segment(document))
print(f"Found {len(sentences)} sentences:")
for i, sent in enumerate(sentences[:5]):  # First 5
    print(f"{i+1}. {sent.strip()}")
```

## Line Breaking

Line breaking determines where text can be wrapped.

### Basic Line Breaking

```python
# Find possible line break positions
text = "This is a very long sentence that might need to be wrapped at some point."
breaks = list(uicu.line_breaks(text))

print(f"Text: '{text}'")
print(f"Possible break positions: {breaks}")

# Visualize break positions
for i, char in enumerate(text):
    if i in breaks:
        print('|', end='')
    print(char, end='')
print()
```

### Language-Specific Line Breaking

```python
# Line breaking rules vary by language
examples = [
    ("Hello world example", "en", "English"),
    ("你好世界示例", "zh", "Chinese"),
    ("こんにちは世界", "ja", "Japanese"),
    ("Привет мир пример", "ru", "Russian"),
]

for text, locale, lang in examples:
    breaks = list(uicu.line_breaks(text, locale=locale))
    print(f"\n{lang}: '{text}'")
    print(f"Break positions: {breaks}")
    
    # Show with markers
    result = ""
    for i, char in enumerate(text):
        if i in breaks and i > 0:
            result += "|"
        result += char
    print(f"With breaks: {result}")
```

### Line Wrapping Implementation

```python
def wrap_text(text, width, locale='en-US'):
    """Wrap text to specified width using Unicode line breaking."""
    if not text or width <= 0:
        return []
    
    breaks = list(uicu.line_breaks(text, locale=locale))
    lines = []
    current_line = ""
    
    for i, char in enumerate(text):
        current_line += char
        
        # Check if we should break here
        if len(current_line) >= width and i + 1 in breaks:
            lines.append(current_line)
            current_line = ""
    
    if current_line:
        lines.append(current_line)
    
    return lines

# Example usage
text = "This is a long paragraph that needs to be wrapped properly according to Unicode line breaking rules."
wrapped = wrap_text(text, 20)
print("Wrapped text:")
for line in wrapped:
    print(f"  '{line}'")
```

## Practical Examples

### Text Statistics

```python
def analyze_text(text, locale='en-US'):
    """Comprehensive text analysis."""
    stats = {
        'characters': len(text),
        'graphemes': len(list(uicu.graphemes(text))),
        'words': len(list(uicu.words(text, locale=locale))),
        'sentences': len(list(uicu.sentences(text, locale=locale))),
        'possible_breaks': len(list(uicu.line_breaks(text, locale=locale))),
    }
    
    # Detailed word analysis
    words = list(uicu.words(text, locale=locale))
    if words:
        stats['avg_word_length'] = sum(len(w) for w in words) / len(words)
        stats['longest_word'] = max(words, key=len)
        stats['shortest_word'] = min(words, key=len)
    
    return stats

# Analyze different texts
texts = [
    ("English", "The quick brown fox jumps over the lazy dog.", "en-US"),
    ("Chinese", "敏捷的棕色狐狸跳过了懒狗。", "zh-CN"),
    ("Mixed", "Hello 世界! 🌍 Welcome to Unicode.", "en-US"),
    ("Emoji", "👨‍👩‍👧‍👦👋🏾 Families are great! 🎉", "en-US"),
]

for name, text, locale in texts:
    print(f"\n{name} Text Analysis:")
    print(f"Text: '{text}'")
    stats = analyze_text(text, locale)
    for key, value in stats.items():
        print(f"  {key}: {value}")
```

### Search and Highlight

```python
def highlight_words(text, search_term, locale='en-US'):
    """Highlight occurrences of words in text."""
    words = list(uicu.words(text, locale=locale))
    word_positions = []
    
    # Find word positions
    pos = 0
    for word in text:
        if text[pos:pos+len(word)] == word:
            word_positions.append((pos, pos + len(word), word))
            pos += len(word)
        else:
            # Skip non-word characters
            while pos < len(text) and text[pos:pos+len(word)] != word:
                pos += 1
    
    # Simple case-insensitive search
    search_lower = search_term.lower()
    highlighted = text
    offset = 0
    
    for start, end, word in word_positions:
        if word.lower() == search_lower:
            # Add highlight markers
            highlighted = (
                highlighted[:start+offset] + 
                f"**{word}**" + 
                highlighted[end+offset:]
            )
            offset += 4  # Length of '**' markers
    
    return highlighted

# Example
text = "The quick brown fox jumps quickly over the lazy fox."
result = highlight_words(text, "fox")
print(f"Original: {text}")
print(f"Highlighted: {result}")
```

### Text Truncation

```python
def smart_truncate(text, max_length, locale='en-US'):
    """Truncate text at word boundaries."""
    if len(text) <= max_length:
        return text
    
    # Find words
    words = list(uicu.words(text, locale=locale))
    if not words:
        return text[:max_length] + "..."
    
    # Build truncated text
    result = ""
    for word in words:
        # Find word in original text to preserve spacing
        word_pos = text.find(word, len(result))
        if word_pos >= 0:
            # Include spacing before word
            next_result = text[:word_pos + len(word)]
            if len(next_result) + 3 > max_length:  # +3 for "..."
                break
            result = next_result
    
    return result.rstrip() + "..."

# Examples
examples = [
    "This is a short text",
    "This is a much longer text that will need to be truncated",
    "NoSpacesHereButStillNeedsTruncation",
    "Mixed English and 中文 text with emoji 🎉",
]

for text in examples:
    truncated = smart_truncate(text, 25)
    print(f"Original ({len(text):2}): '{text}'")
    print(f"Truncated    : '{truncated}'")
    print()
```

### Tokenization for NLP

```python
class TextTokenizer:
    """Tokenizer for natural language processing."""
    
    def __init__(self, locale='en-US'):
        self.locale = locale
        self.word_segmenter = uicu.WordSegmenter(locale)
        self.sentence_segmenter = uicu.SentenceSegmenter(locale)
    
    def tokenize(self, text, level='word'):
        """Tokenize text at specified level."""
        if level == 'grapheme':
            return list(uicu.graphemes(text))
        elif level == 'word':
            return list(self.word_segmenter.segment(text))
        elif level == 'sentence':
            return list(self.sentence_segmenter.segment(text))
        else:
            raise ValueError(f"Unknown level: {level}")
    
    def tokenize_with_positions(self, text):
        """Tokenize and return positions."""
        tokens = []
        for word in self.word_segmenter.segment(text):
            # Find word position (simplified)
            pos = text.find(word)
            if pos >= 0:
                tokens.append({
                    'text': word,
                    'start': pos,
                    'end': pos + len(word),
                    'type': 'word'
                })
        return tokens

# Example usage
tokenizer = TextTokenizer('en-US')
text = "Natural language processing (NLP) is fascinating!"

# Different tokenization levels
print("Tokenization levels:")
for level in ['grapheme', 'word', 'sentence']:
    tokens = tokenizer.tokenize(text, level)
    print(f"  {level}: {len(tokens)} tokens")
    if len(tokens) <= 10:
        print(f"    {tokens}")

# With positions
print("\nTokens with positions:")
tokens = tokenizer.tokenize_with_positions(text)
for token in tokens[:5]:  # First 5
    print(f"  '{token['text']}' at [{token['start']}:{token['end']}]")
```

## Performance Considerations

### Reuse Segmenters

```python
import time

# Compare creating new vs. reusing segmenters
text = "Hello world! " * 1000

# Method 1: Create new segmenter each time
start = time.time()
for _ in range(100):
    words = list(uicu.words(text))
time1 = time.time() - start

# Method 2: Reuse segmenter
segmenter = uicu.WordSegmenter('en-US')
start = time.time()
for _ in range(100):
    words = list(segmenter.segment(text))
time2 = time.time() - start

print(f"New segmenter each time: {time1:.3f}s")
print(f"Reuse segmenter: {time2:.3f}s")
print(f"Speedup: {time1/time2:.1f}x")
```

### Batch Processing

```python
def batch_segment(texts, segmenter):
    """Efficiently segment multiple texts."""
    results = []
    for text in texts:
        # Reuse the same segmenter
        segments = list(segmenter.segment(text))
        results.append(segments)
    return results

# Example
texts = [
    "First sentence here.",
    "Second sentence there.",
    "Third sentence everywhere."
] * 100

segmenter = uicu.SentenceSegmenter('en-US')
results = batch_segment(texts, segmenter)
print(f"Processed {len(results)} texts")
```

## Common Pitfalls and Solutions

### 1. Assuming String Length = Character Count

```python
# Wrong: using len() for character count
text = "👨‍👩‍👧‍👦 Family"
print(f"len(): {len(text)}")  # Wrong!

# Right: use grapheme segmentation
graphemes = list(uicu.graphemes(text))
print(f"Graphemes: {len(graphemes)}")  # Correct!
```

### 2. Word Boundaries in URLs

```python
# URLs need special handling
url = "https://example.com/path/to/page"
words = list(uicu.words(url))
print(f"URL words: {words}")  # Breaks at dots and slashes

# Better: pre-process URLs
def extract_urls(text):
    # Simple URL pattern
    import re
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, text)
    
    # Replace URLs with placeholders
    for i, url in enumerate(urls):
        text = text.replace(url, f"__URL_{i}__")
    
    return text, urls

text = "Visit https://example.com for more info."
cleaned, urls = extract_urls(text)
words = list(uicu.words(cleaned))
print(f"Words: {words}")
print(f"URLs: {urls}")
```

### 3. Locale-Specific Behavior

```python
# Always specify locale for consistent behavior
text = "你好世界"

# Default locale might not handle Chinese well
default_words = list(uicu.words(text))
print(f"Default: {default_words}")

# Chinese locale handles it correctly
chinese_words = list(uicu.words(text, locale='zh-CN'))
print(f"Chinese locale: {chinese_words}")
```

## Next Steps

- Learn about [Transliteration](transliteration.md) for text transformation
- Explore [Date/Time Formatting](date-time-formatting.md) 
- Review [Best Practices](best-practices.md) for text processing