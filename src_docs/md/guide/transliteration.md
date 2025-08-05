---
# this_file: src_docs/md/guide/transliteration.md
title: Transliteration
description: Script conversion and text transformation
---

# Transliteration

UICU provides powerful transliteration capabilities for converting text between different writing systems and applying text transformations.

## Basic Transliteration

Convert between scripts:

```python
import uicu

# Greek to Latin
greek_latin = uicu.Transliterator('Greek-Latin')
greek_text = "Ελληνικά"
latin_result = greek_latin.transliterate(greek_text)
print(f"{greek_text} → {latin_result}")  # Ελληνικά → Ellēniká

# Cyrillic to Latin
cyrillic_latin = uicu.Transliterator('Cyrillic-Latin')
russian_text = "Русский"
result = cyrillic_latin.transliterate(russian_text)
print(f"{russian_text} → {result}")  # Русский → Russkij

# Arabic to Latin
arabic_latin = uicu.Transliterator('Arabic-Latin')
arabic_text = "العربية"
result = arabic_latin.transliterate(arabic_text)
print(f"{arabic_text} → {result}")  # العربية → al'rbyt
```

## Available Transliterators

```python
# List common transliterators
common_transliterators = [
    'Greek-Latin',
    'Cyrillic-Latin', 
    'Arabic-Latin',
    'Hebrew-Latin',
    'Devanagari-Latin',
    'Han-Latin',
    'Hiragana-Latin',
    'Katakana-Latin',
]

test_texts = {
    'Greek-Latin': "Αθήνα",
    'Cyrillic-Latin': "Москва", 
    'Arabic-Latin': "القاهرة",
    'Hebrew-Latin': "ירושלים",
    'Devanagari-Latin': "दिल्ली",
    'Han-Latin': "北京",
    'Hiragana-Latin': "とうきょう",
    'Katakana-Latin': "トウキョウ",
}

for trans_id in common_transliterators:
    if trans_id in test_texts:
        transliterator = uicu.Transliterator(trans_id)
        original = test_texts[trans_id]
        result = transliterator.transliterate(original)
        print(f"{trans_id:18}: {original:8} → {result}")
```

## Bidirectional Transliteration

Some transliterators work in both directions:

```python
# Latin to Greek
latin_greek = uicu.Transliterator('Latin-Greek')
latin_text = "Athena"
greek_result = latin_greek.transliterate(latin_text)
print(f"{latin_text} → {greek_result}")

# Round trip test
greek_latin = uicu.Transliterator('Greek-Latin')
back_to_latin = greek_latin.transliterate(greek_result)
print(f"{greek_result} → {back_to_latin}")
```

## Custom Transformations

```python
# Case transformations
upper_trans = uicu.Transliterator('Any-Upper')
lower_trans = uicu.Transliterator('Any-Lower')
title_trans = uicu.Transliterator('Any-Title')

text = "hello world"
print(f"Upper: {upper_trans.transliterate(text)}")
print(f"Lower: {lower_trans.transliterate(text)}")  
print(f"Title: {title_trans.transliterate(text)}")

# Remove diacritics
nfd_trans = uicu.Transliterator('Any-NFD')
remove_accents = uicu.Transliterator('[:Nonspacing Mark:] Remove')

accented_text = "café naïve résumé"
nfd_result = nfd_trans.transliterate(accented_text)
no_accents = remove_accents.transliterate(nfd_result)
print(f"Original: {accented_text}")
print(f"No accents: {no_accents}")  # cafe naive resume
```

Continue to [Date-Time Formatting](date-time-formatting.md) →