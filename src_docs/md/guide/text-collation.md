---
# this_file: src_docs/md/guide/text-collation.md
title: Text Collation
description: Culture-aware sorting and comparison
---

# Text Collation

Text collation handles sorting, comparison, and searching according to linguistic and cultural rules. UICU's collation engine provides precise control over text ordering.

## Basic Collation

```python
import uicu

# Create a collator for German
german_collator = uicu.Collator('de-DE')

# Sort German names
names = ['Müller', 'Mueller', 'Mahler', 'Möller', 'Zöller']
sorted_names = german_collator.sort(names)
print(f"German sort: {sorted_names}")
# Result: ['Mahler', 'Möller', 'Mueller', 'Müller', 'Zöller']

# Compare strings
result = german_collator.compare('Müller', 'Mueller')
print(f"Müller vs Mueller: {result}")  # 0 = equal in German
```

## Collation Strength

Control comparison sensitivity:

```python
# Different strength levels
text1, text2 = "café", "CAFÉ"

for strength in ['primary', 'secondary', 'tertiary', 'quaternary']:
    collator = uicu.Collator('en-US')
    collator.set_strength(strength)
    result = collator.compare(text1, text2)
    print(f"{strength:12}: {result} ({'equal' if result == 0 else 'different'})")
```

## Numeric Sorting

Handle numbers intelligently:

```python
# Files with numeric sorting
files = ['file10.txt', 'file2.txt', 'file1.txt', 'file20.txt']

# Default string sort
default_sort = sorted(files)
print(f"String sort: {default_sort}")

# Numeric-aware sort
numeric_collator = uicu.Collator('en-US', numeric=True)
numeric_sort = numeric_collator.sort(files)
print(f"Numeric sort: {numeric_sort}")
```

## Advanced Collation Rules

```python
# Custom collation with specific rules
french_collator = uicu.Collator('fr-FR')
french_collator.set_strength('primary')  # Ignore accents primarily
french_collator.set_case_first('lower')  # Lowercase first

words = ['côte', 'Côte', 'cote', 'Cote']
result = french_collator.sort(words)
print(f"French custom: {result}")
```

## Search and Matching

```python
def fuzzy_search(query, documents, locale='en-US', strength='primary'):
    """Locale-aware fuzzy text search"""
    collator = uicu.Collator(locale)
    collator.set_strength(strength)
    
    matches = []
    for doc_id, content in documents.items():
        words = content.split()
        for word in words:
            if collator.compare(query, word) == 0:
                matches.append((doc_id, content))
                break
    return matches

# Search documents
docs = {
    1: "The café serves coffee",
    2: "This cafe has atmosphere", 
    3: "CAFE menu available",
}

results = fuzzy_search("cafe", docs, strength='primary')
print(f"Found {len(results)} matches")
```

Continue to [Text Segmentation](text-segmentation.md) →