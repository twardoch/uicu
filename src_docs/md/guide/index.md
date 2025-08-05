---
# this_file: src_docs/md/guide/index.md
title: User Guide
description: Comprehensive UICU tutorials and guides
---

# User Guide

Welcome to the UICU User Guide! This comprehensive tutorial series will teach you everything you need to know about Unicode text processing with UICU.

## Learning Path

Follow this recommended learning path for the best experience:

### 📚 Fundamentals
1. **[Unicode Basics](unicode-basics.md)** - Essential Unicode concepts
2. **[Character Properties](character-properties.md)** - Deep dive into character analysis

### 🌍 Internationalization  
3. **[Locale Management](locale-management.md)** - Handle 700+ locales
4. **[Text Collation](text-collation.md)** - Culture-aware sorting and comparison

### ✂️ Text Processing
5. **[Text Segmentation](text-segmentation.md)** - Smart text boundary detection
6. **[Transliteration](transliteration.md)** - Script conversion and transformation

### 🕒 Formatting
7. **[Date-Time Formatting](date-time-formatting.md)** - Locale-aware temporal formatting

### 🛡️ Production Ready
8. **[Best Practices](best-practices.md)** - Guidelines for production use

## Quick Reference

| Topic | Key Classes | Use Cases |
|-------|-------------|-----------|
| Character Analysis | `Char` | Input validation, text analysis |
| Locale Support | `Locale` | Internationalization, localization |
| Text Sorting | `Collator` | Search, sorting, comparison |
| Text Breaking | `BreakIterator` | Word wrap, sentence detection |
| Script Conversion | `Transliterator` | Romanization, script conversion |
| Date/Time | `DateFormatter` | Localized date/time display |

## Code Examples

Each guide includes practical examples you can run immediately:

```python
import uicu

# Character analysis
char = uicu.Char('🌍')
print(f"{char.name}: {char.category}")

# Locale-aware sorting
collator = uicu.Collator('de-DE')
sorted_names = collator.sort(['Müller', 'Mueller', 'Mahler'])

# Text segmentation
words = [w.text for w in uicu.words("Hello, world!") if w.is_word]

# Script conversion
trans = uicu.Transliterator('Greek-Latin')
result = trans.transliterate('Ελληνικά')
```

Ready to start? Begin with [Unicode Basics](unicode-basics.md)!