Thanks! I’ll begin by researching and documenting the APIs provided by PyICU and fontTools.unicodedata, especially around Unicode properties, transformations, and writing systems. I’ll also provide a detailed design specification for the new `uicu` package—focusing on a Pythonic, well-structured, and modular API that integrates both libraries’ capabilities and supports grapheme-aware iteration, normalization, script detection, and more.

I’ll let you know once everything is ready for your review.


# Design Plan for the `uicu` Unicode Utilities Library

## Introduction and Background

Python’s built-in `unicodedata` module and ICU (International Components for Unicode) offer comprehensive Unicode support, but using them can be cumbersome or low-level. **PyICU**, the Python bindings for ICU, exposes ICU’s powerful Unicode and internationalization features but through a thin, C++-styled API that isn’t very “Pythonic”. For example, splitting text into grapheme clusters (user-perceived characters) with PyICU requires manual iteration and index tracking in a C++-like fashion. On the other hand, **fontTools.unicodedata** (built on the `unicodedata2` backport) provides up-to-date Unicode data (including script and block properties) but is mostly a set of functions mirroring Python’s `unicodedata` API.

The goal of `uicu` is to combine the strengths of both: wrapping PyICU’s advanced Unicode functionalities in a natural, Pythonic interface, while supplementing with fontTools’ Unicode data for character properties. The result will be a **richly documented, easy-to-use library** that integrates seamlessly with Python’s `str` type but offers much more power. This plan outlines the APIs and design of `uicu` in detail, serving as a guide for implementation.

## Existing APIs Summary

### fontTools.unicodedata (unicodedata2)

FontTools’ `unicodedata` module extends Python’s `unicodedata` with additional information, especially about writing systems (scripts) and blocks. It uses the latest Unicode Character Database via the `unicodedata2` package. Key capabilities include:

* **Up-to-date core properties**: functions like `name(char)`, `category(char)`, `bidirectional(char)`, `combining(char)`, numeric values, normalization, etc., equivalent to Python’s built-in `unicodedata` but updated to the latest Unicode version.
* **Script identification**: `script(char)` returns the four-letter script code for a character (e.g. `'Latn'` for `'a'` and `'Zyyy'` for a comma). `script_extension(char)` returns a **set** of script codes if a character is used in multiple scripts (e.g. U+060C ARABIC COMMA has script extensions `'Arab', 'Thaa', ...` etc.).
* **Script metadata**: `script_name(code)` and `script_code(name)` map between the 4-letter script codes and human-readable script names. Also `script_horizontal_direction(code)` reports text direction (“LTR” or “RTL”) of a given script – for example, it returns `"RTL"` for `"Hebr"` or `"Arab"` and `"LTR"` for `"Latn"`.
* **Block identification**: `block(char)` gives the Unicode block name for the character (e.g. `'Basic Latin'` for `'A'`, `'Arabic'` for an Arabic character, or `'No_Block'` if none).
* **OpenType tag mapping** (for fonts): `ot_tags_from_script(script_code)` and `ot_tag_to_script(tag)` map between Unicode script codes and OpenType script tags.

These APIs provide a **richer Unicode database interface** than the basic `unicodedata` module. We will leverage them in `uicu` to offer script and block info, ensuring our library stays current with new Unicode versions.

### PyICU (Python ICU bindings)

PyICU wraps the ICU C++ libraries, which implement much of the Unicode standard and CLDR (Common Locale Data Repository) functionality. PyICU’s scope includes:

* **Locale-aware transformations**: e.g. case conversions, collation (sorting), formatting dates/numbers, transliteration between writing systems, etc.
* **Unicode algorithms**: e.g. normalization (NFC/NFD etc.), text boundary analysis (grapheme, word, line, sentence segmentation), bidirectional text handling, and more – essentially “big guns” for Unicode processing.
* **Extensive locale data**: ICU knows about various locales’ sorting rules, date/number formats, etc., accessible via PyICU.

However, PyICU’s API closely mirrors ICU’s C++ API, making it less intuitive for Python developers. For instance, to use a break iterator for word boundaries, one must do:

```python
bi = icu.BreakIterator.createWordInstance(icu.Locale('de_DE'))
bi.setText("Ein Beispiel.")
for boundary in bi:
    # boundary is an integer index; need to slice the string manually
    ...
```

As the example suggests, iterating text by words or graphemes requires manual index handling and understanding ICU’s classes. Similarly, to transliterate text, one must instantiate a Transliterator and call its method. While powerful, this approach is not as pythonic or straightforward as it could be.

**PyICU Highlights to Wrap in `uicu`:**

* **Break Iterators**: ICU provides `BreakIterator` factories for **grapheme clusters**, words, sentences, and line breaks. PyICU exposes these via `BreakIterator.createCharacterInstance()`, `createWordInstance()`, etc. and iteration yields boundary indices. We will wrap these to directly yield substrings (e.g. actual grapheme or word strings) to the user.
* **Collation**: ICU’s `Collator` allows locale-aware string comparison and sorting. PyICU’s `Collator.createInstance(locale)` gives a collator; one can then e.g. use `collator.getSortKey(string)` for sorting. We plan to simplify sorting and comparison with an easy interface.
* **Transliteration**: ICU has a rich set of transliterators (script conversions, accent removal, etc.). PyICU exposes `Transliterator.createInstance(id, direction)` and a `.transliterate(str)` method. We will provide a more direct function and class for transliteration.
* **Case Conversion**: ICU handles locale-specific case rules (e.g. Turkish ‘i’). In PyICU, one can use `icu.UnicodeString(text).toLower(locale)` or `toUpper(locale)`. We will wrap these so users can easily do locale-aware case changes on Python strings.
* **Other ICU features**: PyICU also supports formatting (dates, numbers via `DateFormat`, `NumberFormat`), time zones, bidi processing (`Bidi` class), and UnicodeSet/Regex. In this initial plan we focus on text and Unicode-specific features, but our design will be open to adding more (e.g. we might include number/date formatting helpers later).

One important detail: **PyICU handles Python strings by converting them to ICU’s internal UTF-16 representation (UnicodeString)**. Indices returned by ICU (e.g. break positions) count **16-bit code units** – which means Python and ICU indices can differ for characters outside the Basic Multilingual Plane (BMP). For example, an emoji or certain scripts use two 16-bit units in UTF-16 but count as a single character in Python’s str indexing. This can lead to misaligned indices if not handled. Indeed, PyICU users note that when using a native Python `str` with BreakIterator, the boundaries may not align with Python slicing, whereas using ICU’s `UnicodeString` avoids that issue. We will keep this in mind to ensure `uicu` functions return correct results for all Unicode characters (likely by internally using ICU UnicodeString for segmentation tasks).

## Design Goals for `uicu`

1. **Pythonic and Intuitive**: The API should feel natural to Python developers. Common tasks (like iterating over graphemes or words, comparing strings in a locale-aware way, converting text to another script) should be one-liners or simple loops – not requiring manual index arithmetic or obscure ICU constants. We’ll favor Python idioms (iterators, context managers if appropriate, simple functions) over ICU’s class boilerplate.
2. **Leverage ICU Performance**: ICU is written in C/C++ for performance. Our wrapper will call into PyICU (C++ extension) for heavy lifting, ensuring that even though we provide a higher-level interface, it remains efficient. We must be mindful of conversion overhead between Python and ICU (e.g., minimize repeated conversions of large strings).
3. **Comprehensive Unicode Support**: Cover the key features needed for robust Unicode text processing:

   * Character metadata (names, categories, scripts, blocks, numeric values, bidi classes, etc.)
   * Normalization (NFC, NFD, etc. as well as case-folding)
   * Grapheme cluster, word, sentence, and line segmentation
   * Locale-aware case transformations (upper, lower, title)
   * Transliteration between writing systems or transliteration rules
   * Locale-aware collation (comparison and sorting)
   * (Future/optional) Bi-directional text support, regex with Unicode properties, etc.
4. **Integration with Python Types**: Users of `uicu` should primarily work with Python’s built-in types (`str`, possibly `list` for results, etc.) and high-level objects. Internally we may use ICU’s `UnicodeString` or PyICU classes, but the user interface will abstract those away. For example, a user can pass a plain `str` or a locale code as a simple string `"en_US"`, rather than needing to import and use `icu.Locale` explicitly. Return values should be Python strings or collections thereof (except for specialized objects like a Collator instance).
5. **Clean Architecture**: Organize the package into a maintainable structure. Even if initially implemented in a single module `uicu.py`, the code should be modular and logically grouped (we may later split into submodules like `uicu.collation`, `uicu.segmentation`, etc.). We must adhere to the provided project structure, ensuring we have a proper `pyproject.toml`, tests, and documentation files. All public classes/functions need clear docstrings with examples.
6. **Compatibility**: `uicu` will target CPython (since PyICU itself is a CPython extension) and should also work on PyPy (PyICU supports PyPy as well). We will ensure our code doesn’t use any CPython-only API unnecessarily, and rely on PyICU for ICU access.

## Proposed API and Features

Below we detail the key components of `uicu` and how a developer should implement them. We will design `uicu` as a multifile package (if needed) within `src/uicu/`. For clarity, we describe them in categories:

### 1. Unicode Character Properties and Database

**Objective**: Provide easy access to Unicode character information, combining Python’s and ICU’s data.

* **Basic properties**: Functions mirroring `unicodedata` should be provided (or re-exported) for convenience:

  * `uicu.name(char)` – Unicode name of the character, e.g. `"LATIN CAPITAL LETTER A"`. Use `unicodedata.name()` from `unicodedata2` (for up-to-date data) or built-in as fallback.
  * `uicu.category(char)` – General category (e.g. `"Lu"` for uppercase letter).
  * `uicu.bidirectional(char)` – Bidi class (e.g. `"L"` for left-to-right letters).
  * `uicu.combining(char)` – Canonical combining class (integer).
  * `uicu.decimal(char)`, `uicu.digit(char)`, `uicu.numeric(char)` – Numeric values if applicable.
  * `uicu.mirrored(char)` – Whether character is mirrored in bidirectional text.
  * `uicu.east_asian_width(char)` – East Asian width property.
  * `uicu.decomposition(char)` – Decomposition mapping.
    These can directly call `fontTools.unicodedata` (which transparently uses `unicodedata2` or built-in). For example, `uicu.category(c)` can do `return ftunicodedata.category(c)`. The developer should import `fontTools.unicodedata` as, say, `ftunicodedata` at the top of `uicu.py`. (If fontTools/unicodedata2 is not installed, we will document that `uicu` requires it as a dependency – perhaps we list it in `pyproject.toml` extras or include `unicodedata2` as part of installation).

* **Script and block properties**: These are not in Python’s built-in unicodedata, so we expose them via fontTools:

  * `uicu.script(char)` – returns the 4-letter script code of the char (or `"Zzzz"` if unknown).
  * `uicu.script_name(code)` – full English name of a script given its 4-letter code. E.g. `"Latn" -> "Latin"`.
  * `uicu.script_code(name)` – inverse of the above, get script code from name (case-insensitive, ignores spaces/hyphens).
  * `uicu.script_extensions(char)` – returns a **set** of script codes if the char has Script Extensions property. (For chars with a single script, it can return a set with one element, e.g. `{'Latn'}`.)
  * `uicu.block(char)` – Unicode block name as a string (e.g. `'Basic Latin'`).
  * `uicu.block_code(char)` – (Optional) We might define a short code or range for blocks if needed, though just the name is usually enough.
  * **Directionality**: `uicu.script_direction(code)` – returns `"LTR"` or `"RTL"` for a given script code using fontTools’ logic. This can help, for example, to quickly check if text of that script should be rendered right-to-left.

  Implementation: all the above can call corresponding functions in `fontTools.unicodedata`. For example, `uicu.script = ftunicodedata.script`, `uicu.block = ftunicodedata.block`, etc., or use them internally. We should wrap them to handle any necessary type normalization (ensure input `char` is a single-character string or an int codepoint). If a user passes an integer (Unicode code point), we can convert it to `chr(code)` internally to use these functions. This adds pythonic flexibility.

* **Encapsulated Character Object** (optional but encouraged for richness): We can introduce a class `uicu.Char` (or `UnicodeChar`) that represents a single Unicode character and exposes all these properties as attributes. For example:

  ```python
  ch = uicu.Char('您')
  ch.char         # '您'
  ch.name         # 'CJK UNIFIED IDEOGRAPH-60A8'
  ch.category     # 'Lo'
  ch.script       # 'Hani'
  ch.block        # 'CJK Unified Ideographs'
  ch.numeric      # None (not a numeric character)
  ch.bidirectional # 'L'
  ```

  This `Char` class’s `__init__` would take either a one-length string or an integer code point. It can then store the character and lazily compute properties via the above functions (or compute once in constructor). This provides an OO way to bundle character info. It’s not strictly necessary for functionality, but it satisfies the goal of “rich objects” that integrate with Python’s Unicode: the `Char` object could implement `__str__` to return the character, so it prints as the character itself, and maybe `__repr__` to show e.g. `<Char '您' (U+60A8): Name='CJK ...'>`. This can help developers inspect characters easily.

  The junior developer should be guided to implement this class after the functions are in place. Ensure to document each attribute in the class docstring. Also, make it iterable or indexable? Probably not needed (it’s a single char). Comparison between `Char` objects could compare the underlying char. But primarily it's a container for properties.

* **Unicode Version**: We can expose `uicu.unicode_version` indicating the Unicode version of the data (from `unicodedata.unidata_version` which `unicodedata2` provides up-to-date). For completeness, also `uicu.icu_version` via PyICU (perhaps from `icu.ICU_VERSION` if available). These are informational.

**Documentation and Testing**: Document each function with the meaning of returned values (for example, list possible category codes or mention script codes are per ISO 15924). In tests, we should verify a few known values (e.g. `script('A') == 'Latn':contentReference[oaicite:42]{index=42}, script('你') == 'Hani'`, `block('A') == 'Basic Latin':contentReference[oaicite:43]{index=43}`, script\_extensions on a known char, etc.).

### 2. Unicode Normalization and Case Handling

**Normalization**: ICU and Python both support NFC, NFD, NFKC, NFKD normalization. We can simply wrap Python’s `unicodedata.normalize(form, text)` (again from `unicodedata2` for latest data). Provide an easy API:

* `uicu.normalize(text, form='NFC')` – returns the normalized string (form can be "NFC","NFD","NFKC","NFKD"). We can default to NFC as that’s common. This is basically a direct call to `unicodedata.normalize(form, text)`. Include in doc that this uses the latest Unicode data via unicodedata2, so it may recognize characters added in newer versions that the standard library might not (if on older Python).

**Case Folding**: Unicode case folding (for case-insensitive matching) can also be accessed via `unicodedata.normalize("NFKD", s).casefold()` or via ICU’s CaseFold. Simpler: Python’s `str.casefold()` is available (though Python’s casefold should be up-to-date with its Unicode version). We can provide `uicu.casefold(text)` to explicitly use the latest Unicode’s case folding. Implement by simply calling `text.casefold()`. (If we want to be absolutely sure it’s latest, the `unicodedata2` package might have a method for casefold? If not, Python’s will do – casefold doesn’t change often).

**Locale-Aware Case Conversion**: This is where ICU excels beyond Python. Python’s `str.upper()` and `lower()` are **not locale-aware** (they are context-insensitive except for Turkic dotted/dotless i which Python handles in a simplified way via `casefold`). ICU knows, for example, that in Turkish locale, `"i".upper()` should produce `"\u0130"` (Latin capital I with dot). We provide:

* `uicu.to_lower(text, locale=None)`
* `uicu.to_upper(text, locale=None)`
* `uicu.to_title(text, locale=None)`

Each converts the string to the respective case, following the rules of the given locale (if locale is None, use default locale or a root Unicode default). Implement by leveraging ICU’s `UnicodeString` transformations: e.g.

```python
def to_lower(text: str, locale: str = None) -> str:
    # If locale is provided (as BCP47 or ICU format string), get an ICU Locale
    loc = icu.Locale(locale) if locale else icu.Locale()  # default locale
    ustr = icu.UnicodeString(text)
    ustr_lowered = ustr.toLower(loc)
    return str(ustr_lowered)
```

The `icu.UnicodeString.toLower()` will apply locale-specific rules. We then convert back to Python `str` (PyICU allows `str(UnicodeString)` to do that conversion). Similarly for `to_upper` (using `toUpper`) and `to_title`. ICU’s `toTitle` can optionally take a break iterator to define word boundaries (for titlecasing each word), but if not provided, ICU will titlecase the first letter of each word by default. We can accept an optional parameter if needed in future to provide different titlecasing behavior, but not mandatory. Document that these are useful for locales like Turkish (`uicu.to_upper("i", "tr") -> "İ"`, whereas Python’s `"i".upper() -> "I"`). Add tests for such cases.

### 3. Text Segmentation (Graphemes, Words, Sentences, Lines)

One of the most valuable ICU features is splitting text on Unicode boundaries (grapheme cluster, word, etc.), according to the Unicode Text Segmentation standard (UAX #29). We will expose this in a very user-friendly way.

**Grapheme Clusters**: In Python, `for ch in text` iterates code points, not user-visible characters when combined marks are involved. For example, `"🇨🇦"` (Canadian flag emoji) is 2 code points, Python `len("🇨🇦") == 2` and iterating yields two separate regional indicator symbols. We want `uicu.graphemes(text)` to iterate or return the *actual characters* as seen by users.

* Implement `uicu.graphemes(text)` as a generator (or list) of grapheme cluster strings. Internally:

  1. Create an ICU break iterator for *character* boundaries: `bi = icu.BreakIterator.createCharacterInstance(locale)`. Typically, grapheme segmentation isn’t locale-variant (except for certain cases like Hangul syllable breaks, but those are algorithmic). ICU uses root locale if none given. We can allow an optional `locale` arg just in case (default to None).
  2. **Important**: Use ICU’s `UnicodeString` for the text to avoid index issues. E.g. `u16 = icu.UnicodeString(text)`, then `bi.setText(u16)`.
  3. Iterate over `bi` to get break positions (PyICU’s BreakIterator supports Python iteration yielding indices). Collect the segments by slicing the **UnicodeString** at those indices. For each segment `u_segment = u16[i:j]` (PyICU allows slicing a UnicodeString with Python slice syntax), convert it to str and yield.
  4. Alternatively, PyICU might have a convenience: perhaps `for seg in bi.getText()` or similar, but likely not – so we do manual slicing as above.
  5. This yields each grapheme cluster as a Python string.

  We should ensure this handles the entire string (the iterator will yield indices including the final length as end). We stop when `nextBoundary()` returns `-1` (the ICU convention). The last segment from last boundary to end of text must be included. (When using the Python iteration protocol as in `for j in bi:`, I believe it yields the end positions and after loop we’re done – we can manage it as in the blog example: track a `last_pos`, and for each boundary index yield `text[last_pos:j]` then update `last_pos`. But since we have `UnicodeString` and can slice it directly, that approach works similarly, using the UnicodeString for slicing).

  Provide this as both an **iterator** (generator function) and possibly as a method on a higher-level class (if we introduce a `UnicodeString` wrapper class in `uicu`). We could make `uicu.graphemes(text)` return a list for convenience, but for large texts a generator is more memory efficient. Perhaps return an iterator by default; users can do `list(uicu.graphemes(text))` if needed. Document this clearly.

* **Words**: `uicu.words(text, locale=None)` similarly uses `BreakIterator.createWordInstance(locale)`. Word boundary finding is definitely locale-dependent (e.g. Thai, Chinese segmentation). Implementation is analogous: feed a UnicodeString to the break iterator, iterate boundaries, slice out each word. However, note ICU’s definition of “word” will include punctuation and whitespace segments as separate tokens (as seen in the example output where spaces and punctuation came as separate items). We might choose to **filter out non-word tokens** by default – for instance, ICU marks boundaries and you often get empty or whitespace tokens. PyICU’s BreakIterator likely has methods to check the **rule status** to see if a boundary is a word boundary versus whitespace. But to keep it simple, we can initially include everything (so the output list would include spaces/punctuation as separate items, like in the example). Alternatively, we could filter to only alphabetic word tokens by skipping segments that are just whitespace or punctuation. This could be an option flag (e.g. `words(text, skip_delimiters=True)`). For now, perhaps return all segments (as ICU defines them), and mention in docs that punctuation and spaces will appear as separate tokens.

* **Sentences**: `uicu.sentences(text, locale=None)` uses `BreakIterator.createSentenceInstance(locale)`. This will yield sentence by sentence (including the trailing punctuation like period). Implementation is straightforward with slicing like above. Likely we won’t filter anything here; each segment should be a full sentence string.

* **Line Breaks**: `uicu.lines(text, locale=None)` using `BreakIterator.createLineInstance(locale)` for line break opportunities. ICU’s line breaking algorithm identifies places a line can break (considering hyphenation, punctuation, etc.). Typically used for wrapping, but we can expose it similarly. This might include the newline characters if present or potential breaks in text. We should clarify whether we mean *existing* lines or *possible* line break opportunities. Perhaps more useful is splitting on existing newline characters plus ICU’s discretionary breaks. However, as a first pass, we might skip this unless explicitly needed. If included, implement like others.

For all these segmentation functions, to **guide the developer**: write a helper internal function to avoid repetition, e.g. `_break_iterator_segments(text, break_iterator) -> iterator` that given a prepared `BreakIterator` (already set with text) yields substrings. Then each public function (graphemes/words/sentences) can create the appropriate break iterator via PyICU and call this helper. This avoids duplicating the loop logic. The helper can be similar to the pseudocode from ICU examples or our described method. Also, be careful to convert any results to Python str. (PyICU’s UnicodeString slicing yields UnicodeString objects; we should call `str()` on them or ensure iteration yields Python strings directly. Possibly PyICU’s iteration might yield Python str if the BreakIterator was given a Python str… but we gave it UnicodeString. To be safe, explicitly convert segments to str.)

**Locale handling**: If locale is None, use a neutral default. ICU’s `BreakIterator.createXXXInstance(locale)` requires an `icu.Locale` object. We can do `icu.Locale(locale_code)` if a string is given. If None, use `icu.Locale.getDefault()` (current locale) or simply `icu.Locale()` which uses default. Document that locale can influence especially word and sentence boundaries (for example, \`"Mr." might or might not end a sentence depending on locale conventions, etc.).

**Testing**: Use multilingual examples. E.g., grapheme clusters: an emoji with skin tone and ZWJ (👨🏽‍⚕️ as doctor emoji) should count as one grapheme. Korean Hangul syllables vs Jamo sequence should not split, etc. Words: test English (split on spaces/punctuation), CJK (Chinese text should ideally output per Chinese character or idiographic word), and Thai (which has no spaces but ICU should segment Thai words). We might compare results with known correct segmentations for a few cases. Sentence: input with multiple sentences. These tests ensure our wrapper correctly yields expected segments.

### 4. Locale-Aware Collation (String Comparison & Sorting)

Sorting strings in Unicode can be non-trivial (accented letters, different scripts, etc.). ICU’s **Collator** provides proper locale-sensitive ordering (the Unicode Collation Algorithm, UCA). Python’s default sorting is binary/unicode codepoint order which may not be culturally correct. We will create a high-level Collator API in `uicu`:

* **Collator Class**: Introduce `uicu.Collator(locale=None, **options)` as a Pythonic wrapper around ICU’s Collator. This class will encapsulate an ICU collator object (`icu.Collator` or `icu.RuleBasedCollator`). Key methods and usage:

  * `__init__`: Accepts a locale identifier (string or ICU Locale). If None, use default locale. Internally, do `icu.Collator.createInstance(locale_obj)` to get the collator. Also accept optional `options` like **strength** and **case/numeric settings**:

    * `strength`: Unicode collation strength level (primary, secondary, tertiary, quaternary, identical). We can map string or enum values to ICU’s constants. For example, strength="primary" means base letters only (ignore accents and case), "tertiary" is default (distinguish accents and case), etc. If provided, call `collator.setStrength(...)`. PyICU likely exposes an enum or we may use `icu.Collator.PRIMARY` etc.
    * `ignore_case`: If True, set collator to case-insensitive (could set strength to secondary if we want to ignore case differences but keep accents, or use `collator.setAttribute(UCollAttribute.CASE_LEVEL, VALUE_OFF)` accordingly).
    * `numeric`: If True, enable **numeric collation** (so "file2" comes before "file10", treating digits as numbers). ICU allows this via `collator.setAttribute(UCOL_NUMERIC_COLLATION, UCOL_ON)`. If PyICU exposes it, we use it. If not easily, perhaps skip or use a RuleBasedCollator with “\[numeric on]”. But likely PyICU has a way.
    * We can add other options like alternate handling (shifted for punctuation), but to keep it simple for now, these three cover common needs. Document them.

  * **Comparison methods**:

    * `compare(str1, str2) -> int`: return negative if str1 < str2, zero if equal, positive if str1 > str2 under the collation. Implement by calling `self._collator.compare(str1, str2)` if PyICU provides it ( ICU C++ has Collator::compare). If not directly, one can compare sort keys (see below). This is for completeness, though Python typically doesn’t use comparator functions.
    * `key(str) -> object`: return a collation key for the string, suitable for sorting. This could return the raw sort key (often a byte sequence). PyICU’s `collator.getSortKey(str)` returns a Python bytes object that encodes the collation ordering. We can return that directly. These keys, when compared lexicographically (bytewise), reflect the proper order. In usage, one can do `sorted(strings, key=collator.key)`. We might also implement `Collator.__call__(self, s)` to alias to `key(s)`, so that the Collator instance can be passed as a key function directly (since callables are accepted as key in sort). E.g., `sorted(names, key=uicu.Collator('sv_SE'))` to sort Swedish names. This would be very convenient.
    * Perhaps also `__lt__`, `__eq__` methods on Collator that compare two strings? That’s tricky because it’s unclear what to compare to – if we say `collator1 < collator2` doesn’t make sense. We could allow `collator.compare(str1, str2)` usage explicitly. So maybe no need for `__lt__` on Collator itself.

  * **Advanced**: `Collator.sort(list_of_str)` – convenience method to sort a list in place according to that collator. It could just do `list.sort(key=self.key)`. Not essential but a nice one-liner for users.

  * **Rule-based tailoring**: ICU allows custom collation rules (e.g. to change sorting order of certain characters). PyICU has `RuleBasedCollator(rules)`. For completeness, we might allow `Collator(rules="...")` as an alternative way to initialize – detect if the first arg is a string containing collation rules (perhaps if it contains newline or special characters like `&` typical in rules syntax). If so, create `icu.RuleBasedCollator(rules)` instead of locale-based. This is an advanced use-case; we can document but a junior dev can implement by checking an `rules` keyword argument.

  Implementation notes: The Collator wrapper stores `self._collator = icu.Collator.createInstance(loc)` or a RuleBasedCollator. All methods will use this internal `_collator`. We will ensure any string passed to `_collator` is a Python `str`, which PyICU will accept (it converts to UnicodeString under the hood). (If any issues with surrogates, ICU will handle internally in sort key generation correctly.)

* **Functional API**: In addition to the class, provide quick functions:

  * `uicu.sort(strings, locale)` that returns a new list sorted by locale. Implementation: `sorted(strings, key=Collator(locale))`. This is a one-liner using our class. So basically a convenience that hides the Collator object. If we implement it, it should be a shallow wrapper. Example usage: `uicu.sort(["zig", "äpfel", "apple"], locale="de")` and get them sorted as a German would (with "ä" correctly sorted near "a").
  * `uicu.sorted(strings, locale)` similarly (like Python’s built-in `sorted`). One could just use the above, so maybe just one of them is enough.
  * We might also provide `uicu.compare(str1, str2, locale)` for a one-off comparison returning -1/0/1 using a ephemeral Collator. But this is minor; users can instantiate Collator if needed.

**Testing**: We will test that sorting works as expected. For example, sorting \["a", "ä", "b"] in German locale should yield \["a", "ä", "b"] (since ä is treated as a = ae maybe, but in Swedish locale it should come after "z"). We can use known correct orders from examples or ICU docs. Also test numeric collation option: e.g. sorting \["file2", "file10", "file1"] with numeric=True should yield \["file1","file2","file10"], whereas default string collation might give "file1","file10","file2".

### 5. Transliteration and Text Transforms

ICU’s transliteration engine can perform complex text transformations (e.g. converting non-Latin scripts to Latin (romanization), or removing diacritics, etc.). `uicu` will provide easy access to common transliterations and a way to use custom ones:

* **Simple Transliteration Function**: `uicu.transliterate(text, id, direction='forward') -> str`. Here `id` is an ICU transliterator identifier string, like `"Greek-Latin"` to transliterate Greek to Latin script. ICU has many built-in IDs (the ICU user guide lists them). We will not hardcode the list but we can link to ICU docs for reference. `direction` can be `'forward'` (default) or `'reverse'` to apply the inverse transliteration (PyICU expects a constant `icu.UTransDirection.REVERSE` or an enum, but in Python we can just pass a flag). Implementation:

  * If direction is reverse, we could either call `icu.Transliterator.createInstance(id, UTransDirection.REVERSE)`, otherwise the normal createInstance. Apply `.transliterate(text)` and return the result. PyICU will accept Python str for transliteration and return a Python str (likely). If not, we may wrap the text in UnicodeString first just to be safe with any non-BMP issues (though transliteration output length is usually aligned with input characters count or more, but ICU likely handles it).
  * Alternatively, ICU offers an easier reverse: you can get a Transliterator and call `.transpose()` to get inverse. But simply creating with reverse flag is fine.

  This function is a one-liner usage for common tasks. E.g. `uicu.transliterate("Παράδειγμα", "Greek-Latin")` → "Parádeigma".

* **Transliterator Class**: For repeated use or more advanced control, provide a `uicu.Transliterator` class. It will wrap `icu.Transliterator`. Usage:

  ```python
  tr = uicu.Transliterator("Latin-Devanagari")  # create transliterator from Latin script to Devanagari
  hindi = tr.transliterate("kshatriya")  # get result
  tr_rev = tr.inverse()  # get inverse transliterator as a new uicu.Transliterator
  ```

  Implementation:

  * `__init__(self, id, direction='forward')`: store `self._icu_trans = icu.Transliterator.createInstance(id, dir)`. If creation fails (e.g. unknown ID), PyICU might throw an ICUError – catch and raise a custom error or message.
  * `transliterate(self, text)`: simply `return self._icu_trans.transliterate(text)`. PyICU returns a Python str here.
  * `inverse(self)`: returns a new `uicu.Transliterator` which is the inverse of the current. Implement by `inv_icu = self._icu_trans.createInverse()`, then wrap in our class.

  We can also allow custom transliteration rules: ICU supports rule strings to create a Transliterator (for example, a rule that removes diacritics could be `"[\\p{M}]>;"` to strip marks). If user passes a rule string rather than a known ID, ICU will treat it as rules if we call `createInstance` with id. Actually, ICU expects either a registered ID or a rule pattern. There is also `icu.Transliterator.createFromRules(name, rules, direction)` if needed for custom rules not registered. We can expose that via an alternative constructor like classmethod `Transliterator.from_rules(name, rules, direction='forward')`. This might be advanced, but including it would make the API “very extensive” as requested. A junior dev can implement by calling that ICU function.

  Common transliterators to mention in docs: "Any-Latin" (to Latin from any script), "Latin-Ascii" (remove accents), "NFD; \[:Nonspacing Mark:] Remove; NFC" (this can be achieved via rules to strip diacritics if not using built-in). We should encourage using built-in IDs where possible.

* **Other Transforms**: ICU’s transliteration also covers things like case folding (there might be an "Any-CaseFold"), or script-specific transforms like "Hiragana-Katakana". We won’t enumerate all, but by providing the flexible interface, users can do what they need.

**Testing**: Test a couple of transliterations: e.g., Greek to Latin as above, or Devanagari to Latin ("देवनागरी"->"devanāgarī"), and a reverse. Also test using the transliterator object multiple times (to ensure state is either stateless or properly handled – ICU transliterators are usually stateless or reset each call). If we provide custom rule usage, test a simple rule (like swapping letters).

### 6. Additional Considerations

**Error Handling**: PyICU functions throw `ICUError` (a Python exception) when something goes wrong (it wraps ICU’s UErrorCode). For example, if an invalid locale ID or transliterator ID is given, an error will be raised. Our `uicu` can either let these exceptions propagate or catch and wrap them in our own exception class (e.g., define `uicu.Error` as a subclass of Exception, possibly holding the original ICUError). It might be simplest to let ICUError surface, but document it. However, to make a cleaner API, wrapping could be good – for instance, raise `ValueError` for invalid locale or ID, with message extracted from ICUError. A junior developer can implement basic try/except around createInstance calls and raise appropriate Pythonic exceptions (ValueError or a custom UICUError). We should specify this clearly in docs: e.g. "If an unknown script code is requested, a KeyError is raised" (as fontTools does), or "If an invalid transliteration ID is given, `uicu.Error` is raised with the ICU message."

**Performance**: We will advise to **reuse objects** when appropriate. For example, if an application needs to segment many strings the same way, reusing a BreakIterator is more efficient than creating a new one each time (ICU break iterator has an expensive initialization). However, PyICU BreakIterator instances are not obviously reusable with new text (though actually they are: one can call `.setText()` repeatedly on the same iterator with different strings). We might expose that by allowing `uicu.GraphemeIterator` class that holds an ICU BreakIterator and can be called on multiple texts. But that might complicate things for little gain at first. Instead, we can internally cache frequently used break iterators. For instance, `uicu.graphemes` could create a global single `BreakIterator.createCharacterInstance(Locale())` on first use and reuse it (with different text set each call). But ICU break iterators are **not thread-safe** unless each thread has its own. Given this is a library, safer to not cache globally by default (to avoid concurrency issues). Perhaps we skip caching. We can note in documentation that if you need to segment thousands of strings, it may be worth to create a BreakIterator once and reuse via a provided class. As an advanced feature, a `uicu.TextBreaker(kind="word", locale=None)` object could be created, with a method `segments(text)` returning segments. The developer can implement that if needed. Initially, keep it simple: create new ones each call.

For collation, similar reasoning: creating a Collator is somewhat expensive (needs to load collation rules). If sorting many lists, reuse the Collator object. Our API already supports that (via the Collator class).

**Integration with Python iteration and slicing**: We will ensure any custom objects behave intuitively:

* If we have a `uicu.UnicodeString` wrapper (if we decide to create one to mirror ICU’s UnicodeString but as Python class), it should perhaps subclass `str` (so it inherits all string behavior) or at least implement sequence methods (`__len__`, `__getitem__`, etc.) by delegating to the internal str. This might be overkill, and since Python’s str is itself adequate, we probably skip making a custom string type. Instead, we use Python str everywhere and only use ICU’s UnicodeString internally. This is simpler and avoids confusion. So likely we do *not* make a `UnicodeString` class in `uicu` (since Python’s str suffices as the public type). The only new classes we introduce are things like `Char`, `Collator`, `Transliterator` as above, and possibly a `Locale` wrapper if needed.

**Locale Handling**: We should decide whether to expose ICU’s `Locale` class or hide it. PyICU’s Locale can be used directly by users, but to keep things consistent, our functions/classes accept `locale` as either a `str` (like `"en_US"` or `"fr-CA"` or BCP47 `"fr-CA-u-nu-latn"` etc.) or an `icu.Locale` object. Internally, we detect and convert if needed. We may also accept Python’s locale identifiers (which are often the same as ICU, just underscore vs hyphen differences). We'll document using the ICU/CLDR format (language\_Country). Provide convenience like `locale = None` means system default.

We could provide a thin wrapper `uicu.Locale` class that maybe inherits or wraps `icu.Locale` just to add Pythonic methods or repr. However, PyICU’s Locale already has nicely named constructors like `Locale.getFrance()`, etc., and properties like `getDisplayName()`. Probably no need to wrap it deeply. We can simply allow PyICU’s Locale to be used. Maybe just mention in docs that advanced locale info can be accessed via `icu.Locale` if needed, but not necessary for basic usage of our library.

**Package Structure**: The final code will reside under `src/uicu/`. We will have at least `uicu.py` implementing everything in one module for now. We also have `__version__.py` for version info. The project root has README, etc. Ensure to update README.md with usage examples demonstrating our new API (this will help the junior dev and users). Possibly maintain a `TODO.md` with any future extensions (like adding Bidi support or Regex wrappers in future).

If the module grows large, we can refactor into submodules: e.g. `uicu/collation.py`, `uicu/segmentation.py`, etc., and import them in `uicu/__init__.py`. The given structure shows a single `uicu.py`, but a “multifile package” was mentioned, so organizing by feature is okay. For now, the plan can proceed with one file, with clearly separated sections internally and maybe using internal helper functions to keep it tidy.

## Step-by-Step Implementation Guide

Following the design above, here’s a suggested order of implementation for a junior developer:

1. **Set up project structure**: Create the directory and files as given. Ensure `pyproject.toml` has dependencies: include `pyicu` and `fonttools[unicode]` (or `unicodedata2`) as requirements. This ensures the environment has ICU and updated Unicode data. Write a brief README introduction (can be filled after implementing, with examples).

2. **Character properties functions**: In `uicu.py`, import `unicodedata` from `unicodedata2` (fall back to built-in if import fails, but ideally require unicodedata2). Also `from fontTools import unicodedata as ftunicodedata`. Start implementing `name(char)`, `category(char)`, etc., by delegating to these. Write docstrings for each, citing that data is from Unicode X.Y (whatever version). Implement `script`, `block`, etc., using fontTools functions. Make sure to handle if input is not a single character: decide if we want to allow strings of length >1 (maybe not, we can enforce len==1 for these functions, and document that they take a single character). If a longer string is given by mistake, maybe we either process first char or raise an error. Possibly safer to raise ValueError to prevent misuse.

3. **Char class**: Define `class Char:` with an `__init__` that stores the char (after validation) and attributes like name, etc., filled by calling the functions above. This is straightforward. Also define `__repr__` to show meaningful info, and maybe `__str__` to return the raw character. This class goes in `uicu.py` as well.

4. **Normalization and case**: Implement `normalize(text, form)` using `unicodedata.normalize`. Implement `casefold(text)` using `str.casefold()`. Then `to_lower, to_upper, to_title` using PyICU’s UnicodeString as described. For this, you need to import `import icu` at top (PyICU module). If any locale code is provided as argument, convert via `icu.Locale(locale_code)`; if None, use `icu.Locale.getDefault()`. Test these quickly in an interactive session to ensure, for example, `to_upper('i', 'tr_TR')` yields `'\u0130'`. Document these functions with examples.

5. **Segmentation functions**: Import `icu.BreakIterator`. Implement an internal helper, e.g. `_iter_segments(text, bi)` where `bi` is a BreakIterator already set to the text. It should yield segments. Use the pattern:

   ```python
   utext = icu.UnicodeString(text)
   bi.setText(utext)
   last = 0
   for boundary in bi:
       segment = utext[last:boundary]    # get ICU UnicodeString from last to boundary
       yield str(segment)               # convert to Python string
       last = boundary
   ```

   Ensure after the loop, we don’t need an extra step (since the iterator yields the final index equal to text length as the last boundary, the loop logic above actually covers the whole text and ends naturally). Implement `graphemes(text)`, `words(text, locale=None)`, `sentences(text, locale=None)` by creating the appropriate BreakIterator via the class method, then delegating to `_iter_segments`. For locale, if provided (string), do `icu.Locale(locale)`, else default. For word segmentation, consider filtering out purely whitespace tokens: ICU will produce them (see example where spaces are separate). Possibly, we can post-filter: e.g., inside the loop for words, skip `segment` that is all whitespace (or that `segment.strip()` is empty). But sometimes punctuation like "-" might also be separated. We could leave them in to exactly mirror ICU, and let user decide to filter if needed. It’s safer to leave as is for now (complete fidelity), and document that output includes whitespace and punctuation segments.

   Also, ensure that if the text is empty, the functions handle gracefully (probably just yield nothing).

6. **Collator and sorting**: Implement the `Collator` class as described. Import `icu.Collator`. In `__init__`, call `icu.Collator.createInstance(locale_obj)`. If `locale` is a str, do `locale_obj = icu.Locale(locale)`. If that fails (bad locale string), catch ICUError and raise ValueError("Unknown locale ..."). Then set attributes if options given (for strength, etc., use `self._collator.setStrength(icu.Collator.TERTIARY)` for example). PyICU likely has those constants under Collator. If numeric option, try `self._collator.setAttribute(icu.UCollAttribute.NUMERIC_COLLATION, icu.UCollAttributeValue.ON)` – these enums might need import from `icu` as well (PyICU might expose them or via Collator class attributes). Refer to PyICU docs or source for exact usage. If it’s complicated, a simpler workaround is to use a rule-based collator string “\[numeric on]” on top of base rules (as the cheat sheet did for Welsh example), but that's not straightforward for arbitrary locale combination. We expect PyICU Collator to allow setting numeric via `collator.setAttribute`. We’ll proceed with that plan.

   Methods: `compare(a,b)` could use `self._collator.compare(a,b)`. (We should verify PyICU Collator object indeed has a compare method – ICU C++ Collator does. If not, we can simulate by computing keys and comparing those bytewise.) `key(s)` uses `self._collator.getSortKey(s)` which returns `bytes`. That can be returned directly or we might want to return a \_Key wrapper with defined comparison. Simpler: return bytes, since Python will compare those correctly. It’s fine. Implement `__call__ = key` to make the object callable as key function.

   Add a `sort(iterable)` method if desired (just returns sorted copy using self as key).

   Also implement maybe `__enter__` and `__exit__` for context manager? Not obviously needed for Collator. Probably not.

   The developer should also expose a functional interface: define `uicu.sort(strings, locale, **options)` that internally does `return sorted(strings, key=Collator(locale, **options))`. And/or `uicu.sorted` similarly (one might suffice).

   Test the Collator class on a basic example: e.g., `Collator('en').compare("a","b")` returns -1 (assuming "a" < "b"). Sorting with key should order strings properly (we can test with a list including "é" and "e" in French locale, etc.).

7. **Transliteration**: Implement `transliterate(text, id, direction='forward')` function first. Import `icu.Transliterator` and `icu.UTransDirection`. Map `direction='reverse'` to `icu.UTransDirection.REVERSE` (PyICU likely provides this enum). Otherwise use `UTransDirection.FORWARD` or simply omit since forward is default. The call:

   ```python
   trans = icu.Transliterator.createInstance(id, direction_enum)
   result = trans.transliterate(text)
   return result
   ```

   Wrap in try/except to catch ICUError if the ID is invalid, and raise a ValueError listing the id.

   Then the `Transliterator` class: store `self._trans = icu.Transliterator.createInstance(id, dir)`. Provide `transliterate(self, text)` calling `self._trans.transliterate(text)`. Provide `inverse(self)` doing `inv = self._trans.createInverse()` and wrap in `Transliterator` class (i.e., `return Transliterator.__new__` or better provide an alternate constructor: we can simply do `inv_obj = object.__new__(Transliterator)` and set `inv_obj._trans = inv`, but easier is to call our own **init** by constructing a new Transliterator with the reverse param. Actually, simpler: just do `return Transliterator(id, direction='reverse')` if we know id, but that might redo the lookup; using `createInverse` is more direct and handles compound translits properly. So do `inv_icutrans = self._trans.createInverse(); inv = Transliterator.__new__(Transliterator); inv._trans = inv_icutrans; return inv` – and also maybe store an attribute for id or name in the object if needed for reference).

   Additionally, implement `__call__(self, text)` as alias to `transliterate`, so the object can be used as a function (less important, but could be nice).

   Test transliterator on a known transform. If possible, include in tests: for example `uicu.transliterate("ρας", "Greek-Latin")` -> "ras", and inverse returns original (with appropriate direction).

8. **Documentation and Examples**: Throughout the code, add docstrings with examples (in Markdown or reStructuredText if using Sphinx later). E.g., for `uicu.graphemes`: explain what grapheme clusters are, and show usage:

   ```python
   >>> list(uicu.graphemes("naïve"))
   ["n", "ä", "i", "v", "e"]  # the 'a' with diaeresis is one grapheme
   ```

   and perhaps an emoji example. For collation, show sorting example in docstring. For transliteration, show converting script. These will not only help users but also serve as simple tests (could even be used as doctests).

   Update README.md to describe the package and include a quickstart: e.g., demonstrate how to use a few major features (maybe showing a side-by-side of doing something with PyICU vs how much simpler with uicu, to emphasize the improvement). For instance, show how to get grapheme clusters in one line with `list(uicu.graphemes(text))` instead of 10 lines of PyICU code.

9. **Testing**: In `tests/test_package.py`, write tests for each major function. Use assertions for known values. For segmentation, you might include known tricky cases (like flags, family emojis 👨‍👩‍👦, which should count as one grapheme each). For collation, test that Collator sorts strings in expected order for a couple of locales. Note: Running ICU collation tests might require known reference data; we can do a simpler test like sorting `["Z", "a"]` in a case-insensitive Collator and expecting `["a","Z"]` when strength=primary (ignoring case). Transliteration test as mentioned. Character property tests using a couple of characters from different scripts.

10. **Performance check** (optional): If possible, benchmark that calling our functions isn’t egregiously slow. Likely fine, but if issues, consider optimizations (like caching ICU objects). Since this is an initial version, clarity and correctness come first; optimizations can be listed in TODO.md.

By following this plan, the junior developer should be able to implement `uicu` as a well-organized package. The end result will be a multi-faceted Unicode utility library that harnesses ICU’s power with a clean Python interface. This will greatly simplify tasks such as iteration over graphemes (previously “more of a pain than you’d hope” in raw PyICU), handling full Unicode properties, and performing locale-aware text processing in Python.

## Package Structure Confirmation

The `uicu` package will conform to the given structure. All code resides in `src/uicu/`, primarily in `uicu.py` (which can import submodules if we split the code). We will include the version in `__version__.py`. Tests in `tests/`. Documentation in `README.md` and possibly supplementary design notes in `AGENTS.md`/`CLAUDE.md` if those are used for project communication.

After implementation, the developer should verify everything is running using the latest ICU (PyICU) and fontTools data. We expect that this library will make advanced Unicode handling in Python much more accessible, combining **the extensive ICU functionality** with **Pythonic ease of use**.

**Sources:** This plan was informed by ICU/PyICU documentation and examples, as well as fontTools’ Unicode data module reference.
