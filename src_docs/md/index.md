---
# this_file: src_docs/md/index.md
title: UICU Documentation
description: A Pythonic wrapper around PyICU with supplementary Unicode functionality
---

# UICU - Unicode International Components for You

Welcome to **UICU**, a Pythonic wrapper around PyICU that makes Unicode text processing intuitive and powerful.

## Table of Contents & TLDR

This documentation is organized into **9 comprehensive chapters** that guide you from basic installation to advanced Unicode processing:

### :material-rocket-launch: Chapter 1: [Getting Started](getting-started.md)
**TLDR**: Quick installation and your first UICU operations  
Learn how to install UICU and run your first Unicode operations in minutes. Covers pip installation, basic imports, and simple character analysis.

### :material-download: Chapter 2: [Installation](installation.md)
**TLDR**: Detailed setup instructions for all platforms  
Complete installation guide including system requirements, PyICU dependencies, virtual environments, and troubleshooting common setup issues.

### :material-unicode: Chapter 3: [Unicode Basics](guide/unicode-basics.md)
**TLDR**: Essential Unicode concepts and UICU's approach  
Foundation concepts including Unicode standards, encodings, normalization, and how UICU simplifies complex Unicode operations.

### :material-tag-text: Chapter 4: [Character Properties](guide/character-properties.md)
**TLDR**: Rich character information and analysis  
Deep dive into Unicode character properties, scripts, blocks, categories, and UICU's intuitive `Char` class for character analysis.

### :material-earth: Chapter 5: [Locale Management](guide/locale-management.md)
**TLDR**: Internationalization with 700+ locales  
Comprehensive guide to locale-aware operations, cultural adaptations, and region-specific text processing across different languages.

### :material-sort-alphabetical: Chapter 6: [Text Collation](guide/text-collation.md)
**TLDR**: Culture-aware sorting and comparison  
Master text sorting, comparison, and searching with locale-specific rules, numeric sorting, and custom collation strength.

### :material-text-search: Chapter 7: [Text Segmentation](guide/text-segmentation.md)
**TLDR**: Smart text breaking and boundary detection  
Learn to properly segment text into graphemes, words, sentences, and lines following Unicode Text Segmentation standard.

### :material-swap-horizontal: Chapter 8: [Transliteration](guide/transliteration.md)
**TLDR**: Script conversion and text transformation  
Convert between writing systems, romanize non-Latin scripts, and perform intelligent text transformations.

### :material-calendar-clock: Chapter 9: [Date-Time Formatting](guide/date-time-formatting.md)
**TLDR**: Locale-aware date and time presentation  
Format dates, times, and numbers according to local conventions with full internationalization support.

---

## Why UICU?

UICU transforms the powerful but complex PyICU library into a natural, Pythonic experience:

```python
import uicu

# 🔍 Rich Unicode character information
char = uicu.Char('€')
print(f"{char.name}: {char.category}")  # EURO SIGN: Sc

# 🌍 Locale-aware sorting (German rules)
collator = uicu.Collator('de-DE')
words = ['Müller', 'Mueller', 'Mahler']
print(collator.sort(words))  # Proper German ordering

# ✂️ Smart text segmentation
text = "👨‍👩‍👧‍👦 is a family."
print(list(uicu.graphemes(text)))  # ['👨‍👩‍👧‍👦', ' ', 'i', 's', ...]

# 🔄 Script conversion
trans = uicu.Transliterator('Greek-Latin')
print(trans.transliterate('Ελληνικά'))  # 'Ellēniká'
```

## Key Features

### 🎯 Pythonic API
Natural Python interfaces replace PyICU's C++-style API, making Unicode accessible to all Python developers.

### ⚡ High Performance
Built on ICU's optimized C++ implementation, UICU delivers blazing-fast Unicode operations with minimal overhead.

### 🌐 Comprehensive Coverage
- **700+ Locales**: Full internationalization support
- **Unicode 15.0**: Latest standard compliance
- **Rich APIs**: Character properties, collation, segmentation, transliteration, and more

### 🔧 Production Ready
- **Type Safe**: Full type hints for better IDE support
- **Well Tested**: Comprehensive test suite with high coverage
- **Documented**: Clear examples and API documentation

## Quick Navigation

<div class="grid cards" markdown>

-   :material-school:{ .lg .middle } **[User Guide](guide/index.md)**

    ---

    Master UICU's features with comprehensive tutorials and examples

-   :material-api:{ .lg .middle } **[API Reference](api/index.md)**

    ---

    Detailed API documentation with method signatures and examples

-   :material-code-tags:{ .lg .middle } **[Examples](examples/index.md)**

    ---

    Real-world usage examples and code snippets

-   :material-wrench:{ .lg .middle } **[Development](development/index.md)**

    ---

    Contributing guide and development setup

</div>

## Community & Support

- **GitHub**: [github.com/twardoch/uicu](https://github.com/twardoch/uicu)
- **PyPI**: [pypi.org/project/uicu](https://pypi.org/project/uicu)
- **Issues**: [Report bugs or request features](https://github.com/twardoch/uicu/issues)

## License

UICU is licensed under the MIT License. See the [License](about/license.md) page for details.