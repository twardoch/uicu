Create

# Specification for `uicu`: A Pythonic Internationalization Library

## Part 1: Analysis of Foundation Libraries & Rationale for `uicu`

The landscape of Python internationalization (i18n) is dominated by powerful,
yet often inaccessible, tools. While the standard library provides basic
Unicode support, complex, locale-sensitive operations require more specialized
libraries. The most comprehensive of these is `PyICU`, a Python binding for
the industry-standard "International Components for Unicode" (ICU) C++
libraries. ICU is the gold standard for i18n, implementing vast portions of
the Unicode Standard and the Common Locale Data Repository (CLDR). However,
`PyICU`'s power is encumbered by an Application Programming Interface (API)
that is fundamentally un-pythonic, creating a significant barrier to adoption
and effective use.

This specification details the design of `uicu`, a new Python library that
serves as a high-level, pythonic wrapper around `PyICU`. `uicu` is not a
replacement for `PyICU` but a carefully designed abstraction layer. Its goal
is to expose the full power of the ICU engine through an API that is natural,
intuitive, and seamlessly integrated with the Python language and its
ecosystem. Furthermore, where `PyICU`'s data is incomplete or less accessible,
particularly concerning script and writing system metadata, `uicu` will
strategically supplement its functionality with the `fontTools.unicodedata`
module, which provides access to the most current Unicode data. This document
provides a complete architectural blueprint for `uicu`, intended to guide its
implementation by a developer.

### 1.1 An Autopsy of the PyICU API: Power Encumbered by a C++ Legacy

To understand the necessity for `uicu`, one must first perform a critical
analysis of `PyICU`. The library is not flawed in its core function—it
successfully exposes the vast capabilities of ICU to Python. Its primary
deficiency lies in its design philosophy, which prioritizes a direct, one-to-
one mapping from the underlying C++ library over Python developer ergonomics.
This results in an API that feels alien to seasoned Python developers and
presents a steep learning curve for newcomers.

#### 1.1.1 The C++ Mirror

The `PyICU` API is, by design, a thin wrapper around the ICU4C C++ library.
There is no official API documentation for `PyICU` itself; the documentation
explicitly directs users to the ICU4C C++ API reference and provides a set of
translation patterns. This design choice has profound consequences for the
user experience:  

  * **Class Naming:** Class names are lifted directly from C++, resulting in `PascalCase` names like `Transliterator`, `BreakIterator`, `Collator`, and `DateFormat`, which deviate from Python's PEP 8 convention of `CapWords` for classes but are often used in contexts where `snake_case` functions would be more appropriate.  

  * **Method Naming:** Method names also follow the C++ `camelCase` convention (e.g., `getDisplayName`, `createInstance`, `nextBoundary`) rather than Python's `snake_case`.

  *  **Enumerations:** `PyICU` uses C-style enumerations, such as `icu.DateFormat.LONG` or `icu.UTransDirection.REVERSE`, which are represented as integer constants. A pythonic approach would favor string literals (`'long'`) or `Enum` types for better readability and self-documentation.

This direct mapping forces the Python developer to learn and operate within a
C++ paradigm, constantly translating concepts and consulting external, non-
Python documentation to perform even basic tasks.

#### 1.1.2 A Catalogue of Pythonic Anti-Patterns

The friction caused by `PyICU` extends beyond naming conventions into
fundamental API design patterns that conflict with established Python idioms.
The following examples represent the most significant sources of this
friction.

  *  **Mutable`UnicodeString` and In-Place Modification:** Python's native `str` type is immutable, a cornerstone of its design that ensures predictability and safety. In stark contrast, `PyICU`'s primary string type, `UnicodeString`, is mutable. This leads to one of the most un-pythonic patterns in the library: functions that modify arguments in-place. This "output parameter" pattern, common in C and C++, is highly unconventional in Python.

For example, to get the display name of a locale, the "ICU way" involves
passing a mutable `UnicodeString` object to be modified:

Python

    
        # PyICU: In-place modification (un-pythonic)
    from icu import UnicodeString, Locale
    locale = Locale('pt_BR')
    string_buffer = UnicodeString()
    name = locale.getDisplayName(string_buffer)
    # `name` is the same object as `string_buffer`, which has been modified.
    # name is string_buffer -> True
    

While `PyICU` often provides a more "Python way" that allocates a new string,
the existence and documentation of the in-place modification pattern is a
source of confusion and potential bugs. It violates the principle that
functions should return results without causing side effects on their
arguments.

  *  **Cumbersome Iteration:** Python's `for` loop is a powerful and elegant construct for iteration. `PyICU`'s iteration mechanisms, however, are low-level and stateful, requiring manual bookkeeping. The `BreakIterator`, used for segmenting text into words, sentences, or graphemes, is a prime example. Its usage is described as "a pain" and requires the developer to manually call `nextBoundary()` and track indices.

Python

    
        # PyICU: Manual, stateful iteration
    from icu import BreakIterator, Locale
    text = 'Bist du in der U-Bahn geboren?'
    de_words = BreakIterator.createWordInstance(Locale('de_DE'))
    de_words.setText(text)
    
    words =
    last_pos = 0
    while True:
        next_boundary = de_words.nextBoundary()
        if next_boundary == -1:
            break
        words.append(text[last_pos:next_boundary])
        last_pos = next_boundary
    # words ->
    

A Python developer expects a simple generator or an object that implements the
iterator protocol, allowing for `for word in segmenter:...`. Similarly, the
`StringEnumeration` object provides three different `next` methods (`next`,
`unext`, `snext`) for retrieving different string types, adding another layer
of complexity to what should be a straightforward iteration.

  *  **Opaque Type Conversions:** The library performs some automatic type conversions to bridge the gap between Python and ICU types. For instance, it converts Python `datetime` objects and numeric timestamps into ICU's `UDate` format (a float representing milliseconds since the Unix epoch). While intended as a convenience, this implicit magic can obscure what is happening under the hood. A float passed to a date function is automatically multiplied by 1000, a detail a developer must remember to correctly interpret the underlying `UDate` value. A pythonic library should either be explicit about its conversions or handle them so transparently that the user never needs to be aware of the internal types.

  *  **Generic Error Handling:** `PyICU` commendably translates ICU's C-style `UErrorCode` status values into a Python exception, `ICUError`. This is a significant improvement over checking return codes. However, using a single, generic exception type for the entire library is a missed opportunity. The ICU library can fail for hundreds of different reasons, from a malformed locale string to an invalid formatting pattern. A single `ICUError` forces the developer to parse the error message string to determine the cause of failure, making robust, programmatic error handling difficult.

The cumulative effect of these anti-patterns is a developer experience fraught
with friction. The initial hurdle of installing `PyICU`, which often requires
manual configuration of C++ compilers and library paths due to its dependency
on the ICU C++ libraries, is substantial. For a developer to overcome this
barrier only to be met with a non-intuitive API that requires consulting C++
documentation is a significant deterrent. This compounding friction
discourages the use of ICU's powerful features in the Python ecosystem. The
primary value of `uicu` is to eliminate this second, API-level barrier, thus
making the initial investment in installation a much more reasonable
proposition.

PyICU Anti-Pattern

|

Example `PyICU` Code

|

Problem Description

|

`uicu` Design Principle

|

Proposed `uicu` Code  
  
---|---|---|---|---  
  
In-place argument modification

|

`name = locale.getDisplayName(string_buffer)`

|

Violates Python's convention of immutability and functional returns. Confusing
and error-prone.

|

Immutability and Functional Returns

|

`name = locale.display_name()`  
  
Stateful, manual iteration

|

`while True: boundary = bi.nextBoundary()`

|

Verbose, low-level, and requires manual state tracking. Unnatural for Python
developers.

|

Iterable and Generator-based APIs

|

`for word in segmenter.segment(text):...`  
  
Verbose factory methods with constants

|

`df = DateFormat.createDateInstance(DateFormat.LONG, locale)`

|

Relies on C-style integer constants. Not self-documenting.

|

Object-Oriented Factories with String Keywords

|

`df = locale.get_date_formatter(style='long')`  
  
Ambiguous `key` function for sorting

|

`sorted(L, key=collator.getSortKey)`

|

The method name `getSortKey` is explicit but verbose. The object itself should
be the key.

|

Leverage Dunder Methods (`__call__`)

|

`sorted(L, key=my_collator)`  
  
Generic exception type

|

`except ICUError as e: if "U_ILLEGAL_ARGUMENT_ERROR" in str(e):...`

|

Prevents specific, programmatic error handling. Requires fragile string
parsing of error messages.

|

Rich, Specific Exception Hierarchy

|

`except uicu.ConfigurationError as e:...`  
  
Export to Sheets

#### 1.1.3 Core Functionality Mapping

Despite its challenging API, `PyICU` provides access to an unparalleled suite
of internationalization services. A successful wrapper must recognize and
preserve this power. The key functional domains of `PyICU` that `uicu` will
abstract include:

  *  **Locale:** Handling locale identifiers and providing access to locale-specific data (`icu.Locale`).

  *  **Collation:** Performing locale-sensitive string sorting (`icu.Collator`, `icu.RuleBasedCollator`).

  *  **Formatting:** Formatting dates, times, numbers, currencies, and lists according to locale conventions (`icu.DateFormat`, `icu.NumberFormat`, `icu.ListFormatter`).  

  * **Message Formatting:** Handling pluralization and gender in translated strings (`icu.MessageFormat`).  

  * **Transliteration:** Converting text between different scripts (e.g., Cyrillic to Latin) (`icu.Transliterator`).

  *  **Segmentation:** Breaking text into its logical components like graphemes, words, or sentences (`icu.BreakIterator`).

  *  **Time Zones:** Accessing ICU's comprehensive time zone database (`icu.TimeZone`, `icu.ICUtzinfo`).

`uicu`'s mission is to liberate this functionality, making it accessible
through a clean, pythonic interface.

### 1.2 The Strategic Role of `fontTools.unicodedata`

While `PyICU` is the primary engine for locale-sensitive operations, it is not
the ideal source for all Unicode character data. For this, `uicu` will turn to
`fontTools.unicodedata`, a module within the powerful `fontTools` library.
This is a strategic choice based on data currency, functional specialization,
and API quality.

#### 1.2.1 Decoupling from the Python Runtime

Python's standard library includes a `unicodedata` module. However, the
version of the Unicode Character Database (UCD) it contains is fixed to the
version of the Python interpreter itself. An application running on Python 3.9
will have an older UCD than one on Python 3.12. This can lead to
inconsistencies and an inability to work with the latest characters and
properties.

The `fontTools` library, when installed with the `[unicode]` extra, depends on
`unicodedata2`. `unicodedata2` is a standalone package whose versions are
explicitly tied to Unicode standard versions (e.g., `unicodedata2==15.0.0`
contains data from Unicode 15.0). By using `fontTools.unicodedata`, `uicu`
ensures that developers can access up-to-date Unicode data, independent of the
Python runtime they are using.

#### 1.2.2 Rich Script and Writing System Metadata

The most compelling reason to use `fontTools.unicodedata` is its specialized
functionality related to writing systems, a domain critical for typography and
advanced text processing. It provides a clean, direct API for accessing
properties that are not as easily surfaced through `PyICU`. Key functions
include :  

  * `script(char)`: Returns the four-letter ISO 15924 script code for a character (e.g., `'Latn'`, `'Cyrl'`).

  * `script_name(script_code)`: Converts a script code to its human-readable name (e.g., `'Latn'` -> `'Latin'`).

  * `block(char)`: Returns the Unicode block a character belongs to (e.g., `'Basic Latin'`).

  * `ot_tags_from_script(script_code)`: Provides the crucial mapping from a Unicode script code to its corresponding OpenType script tag(s), essential for font feature interaction.

  * `ot_tag_to_script(tag)`: Provides the reverse mapping.

This functionality directly addresses the needs of applications that go beyond
simple string comparison and formatting into the realm of text layout and font
manipulation.

#### 1.2.3 API Consistency

The API of `fontTools.unicodedata` is simple, functional, and pythonic. It
consists of straightforward functions that take a character or code and return
a result. This design philosophy serves as a model for the non-locale-
sensitive parts of `uicu`, reinforcing the goal of creating a clean and
predictable developer experience.

The use of both `PyICU` and `fontTools.unicodedata` introduces a potential for
inconsistency, as the Unicode data may come from two different sources (the
version of `libicu` linked by `PyICU` and the version of `unicodedata2` used
by `fontTools`). An application dealing with internationalization requires a
single, authoritative source of truth. A subtle bug could arise if a character
property check using one library yields a different result from a check using
the other.

To mitigate this, `uicu` will establish a clear "chain of command" for data
access. For general, non-locale-specific Unicode character properties (e.g.,
name, category, numeric value, script, block), `uicu` will default to
`fontTools.unicodedata` as the primary source, ensuring access to the latest
Unicode standard data. For all locale-sensitive operations (e.g., collation,
date/number formatting, segmentation), `uicu` will exclusively use the `PyICU`
engine, which relies on the comprehensive CLDR data bundled with ICU. This
hybrid approach, clearly defined and documented, provides the best of both
worlds: the most current character data and the most powerful i18n engine.

## Part 2: The `uicu` Library: A Detailed Specification

This section provides the complete architectural and API design for the `uicu`
library. It is intended to be a prescriptive blueprint for implementation,
detailing the structure, classes, methods, and behavior of the new library.

### 2.1 Guiding Principles of the `uicu` API

The design of `uicu` is governed by a set of core principles aimed at creating
an API that is powerful, discoverable, and above all, pythonic. These
principles are a direct response to the shortcomings identified in the `PyICU`
API and are informed by best practices in modern Python library design.

#### 2.1.1 The Pythonic Contract

  *  **Naming Conventions:** All public-facing modules, classes, functions, and methods will strictly adhere to PEP 8 naming conventions. Modules and functions will use `snake_case` (e.g., `uicu.collate`, `uicu.char.get_name`). Classes will use `CapWords` (e.g., `uicu.Locale`, `uicu.format.NumberFormatter`). This provides immediate visual consistency with the broader Python ecosystem.

  *  **Immutability by Default:** Where possible, objects will be immutable. Configuration objects like formatters and collators, once created and configured, will not be modifiable. All functions and methods will return new, native Python objects (`str`, `tuple`, `datetime.datetime`) rather than modifying arguments in-place or returning special wrapper types. This promotes a functional style and prevents unexpected side effects.

  *  **Native Type Integration:** The entire public API surface will exclusively accept and return standard Python types. A user will never need to instantiate or handle a `PyICU.UnicodeString` or be aware of the `UDate` timestamp format. All necessary conversions will be handled transparently within the `uicu` wrapper.

  *  **Leveraging the Language:** The library will make extensive use of Python's special "dunder" methods to make its objects behave intuitively. For example, segmenter objects will be iterable (`__iter__`), collator objects will be callable (`__call__`), and all objects will have useful string representations (`__str__`, `__repr__`).

#### 2.1.2 A Coherent, Object-Oriented Model

`uicu` will be structured around a clear, object-oriented model where objects
represent configured "service providers." Instead of a procedural approach
with standalone functions, the primary workflow will involve:

  1. Instantiating a central `uicu.Locale` object to define context.

  2. Using this `Locale` object as a factory to create specialized, locale-aware service objects (e.g., a `Collator` or `DateTimeFormatter`).

  3. Calling methods on these service objects to perform operations.

This pattern promotes encapsulation, reusability, and thread safety, as
configured service objects can be created once and used many times.

#### 2.1.3 A Rich Exception Hierarchy

To enable robust and specific error handling, `uicu` will define its own
exception hierarchy, inheriting from a common base exception. This allows
consumers of the library to write fine-grained `try...except` blocks, a
significant improvement over `PyICU`'s single `ICUError`.

The proposed hierarchy is:

  * `uicu.Error(Exception)`: The base exception for all errors originating from the `uicu` library.

    * `uicu.ConfigurationError(uicu.Error)`: Raised for errors during setup, such as providing an invalid locale identifier or a malformed rule string.

    * `uicu.FormattingError(uicu.Error)`: Raised by any of the formatters in the `uicu.format` sub-package for invalid patterns or inputs.

    * `uicu.CollationError(uicu.Error)`: Raised by the `uicu.collate` module for issues related to collation rules.

    * `uicu.SegmentationError(uicu.Error)`: Raised by the `uicu.segment` module.

    * `uicu.TransliterationError(uicu.Error)`: Raised for invalid transliteration IDs or rules.

Module/Class

|

Core Purpose

|

Key Method/Usage

|

Abstracts `PyICU` Component  
  
---|---|---|---  
  
`uicu.char`

|

Provides access to non-locale-specific Unicode character properties.

|

`uicu.char.script('A')`

|

`fontTools.unicodedata`  
  
`uicu.locale.Locale`

|

Represents a specific locale and acts as a factory for locale-sensitive
services.

|

`locale = uicu.Locale('de-DE')`

|

`icu.Locale`  
  
`uicu.collate.Collator`

|

Provides locale-sensitive string comparison for sorting.

|

`sorted(L, key=collator)`

|

`icu.Collator`  
  
`uicu.format.DateTimeFormatter`

|

Formats `datetime` objects into locale-specific strings.

|

`formatter.format(datetime.now())`

|

`icu.DateFormat`  
  
`uicu.format.NumberFormatter`

|

Formats numbers, currencies, and percentages.

|

`formatter.format_currency(123.45, 'EUR')`

|

`icu.NumberFormat`  
  
`uicu.format.ListFormatter`

|

Joins a list of strings with locale-correct conjunctions.

|

`formatter.format(['a', 'b', 'c'])`

|

`icu.ListFormatter`  
  
`uicu.segment.WordSegmenter`

|

Segments text into words according to locale-specific rules.

|

`for word in segmenter.segment(text):...`

|

`icu.BreakIterator`  
  
`uicu.translit`

|

Provides functions for script transliteration.

|

`uicu.translit.transliterate(text, 'Cyrl-Latn')`

|

`icu.Transliterator`  
  
Export to Sheets

### 2.2 The `uicu.char` Module: A Unified View of Character Properties

This module will serve as the single, authoritative source for non-locale-
sensitive Unicode character data, implementing the "Data Authority Principle."
It will primarily delegate to `fontTools.unicodedata` to ensure access to the
latest Unicode version data.  

**Functions:**

All functions will take a single argument, `char`, which must be a string of
length 1. They will raise a `ValueError` if the string is not of length 1.

  * `name(char: str, default: Any =...) -> str`: Returns the official Unicode name for the character. If no name exists and a default is provided, returns the default; otherwise, raises a `KeyError`.

  * `category(char: str) -> str`: Returns the two-letter general category abbreviation (e.g., 'Lu', 'Nd', 'Po').

  * `numeric(char: str, default: Any =...) -> Union[int, float]`: Returns the numeric value of the character.

  * `script(char: str) -> str`: Returns the four-letter ISO 15924 script code (e.g., 'Latn').

  * `script_name(char: str) -> str`: Returns the human-readable script name (e.g., 'Latin').

  * `block(char: str) -> str`: Returns the name of the Unicode block the character belongs to.

  * `bidirectional(char: str) -> str`: Returns the bidirectional class (e.g., 'L', 'R', 'AN').

  * `combining(char: str) -> int`: Returns the canonical combining class as an integer.

  * `mirrored(char: str) -> bool`: Returns `True` if the character is a mirrored character in bidirectional text.

  * `is_private_use(char: str) -> bool`: Checks if the character is in a Private Use Area.

  * `is_control(char: str) -> bool`: Checks if the character is a C0 or C1 control code.

### 2.3 The `uicu.locale` Module: The Contextual Heart of the Library

This module defines the `Locale` class, which is the central entry point for
all locale-sensitive operations. It encapsulates a specific locale and acts as
a factory for service objects.

 **`uicu.Locale` Class:**

  *  **`__init__(self, locale_identifier: str)`**

    * Accepts a locale identifier string in BCP 47 format (e.g., `'en-GB'`, `'fr-CA'`, `'zh-Hant-TW'`).

    * The constructor will immediately call the underlying `icu.Locale.canonicalize` to validate and normalize the identifier, raising `uicu.ConfigurationError` on failure.

    * Internally stores the canonicalized `icu.Locale` object.

  *  **Properties (read-only):**

    * `display_name` -> `str`: The full, human-readable name of the locale in the default system locale's language (e.g., `'English (United Kingdom)'`).

    * `language_display_name` -> `str`: The human-readable name of the language (e.g., `'English'`).

    * `script_display_name` -> `str`: The human-readable name of the script.

    * `region_display_name` -> `str`: The human-readable name of the region.

    * `language` -> `str`: The two- or three-letter language code (e.g., `'en'`).

    * `script` -> `str`: The four-letter script code (e.g., `'Latn'`).

    * `region` -> `str`: The two-letter or three-digit region code (e.g., `'GB'`).

    * `base_name` -> `str`: The string representation of the canonicalized locale identifier.

  *  **Factory Methods:**

    * `get_collator(...) -> uicu.collate.Collator`: Returns a configured `Collator` object for this locale.

    * `get_datetime_formatter(...) -> uicu.format.DateTimeFormatter`: Returns a `DateTimeFormatter`.

    * `get_date_formatter(...) -> uicu.format.DateTimeFormatter`: A convenience for a date-only formatter.

    * `get_time_formatter(...) -> uicu.format.DateTimeFormatter`: A convenience for a time-only formatter.

    * `get_number_formatter(...) -> uicu.format.NumberFormatter`: Returns a `NumberFormatter`.

    * `get_list_formatter(...) -> uicu.format.ListFormatter`: Returns a `ListFormatter`.

    * `get_message_formatter(pattern: str) -> uicu.format.MessageFormatter`: Returns a `MessageFormatter` for a given pattern string.

    * `get_grapheme_segmenter() -> uicu.segment.GraphemeSegmenter`: Returns a segmenter for grapheme clusters.

    * `get_word_segmenter() -> uicu.segment.WordSegmenter`: Returns a segmenter for words.

    * `get_sentence_segmenter() -> uicu.segment.SentenceSegmenter`: Returns a segmenter for sentences.

### 2.4 The `uicu.collate` Module: Pythonic Sorting

This module provides an intuitive interface to ICU's powerful collation
engine.

 **`uicu.Collator` Class:**

This class is designed to be used directly as a `key` in sorting functions.

  *  **Instantiation:** Should not be instantiated directly. Use `locale.get_collator()`.

  *  **`__call__(self, text: str) -> bytes`:**

    * This is the core method. It takes a Python string and returns a binary sort key. When used as `sorted(my_list, key=my_collator)`, Python's sorting algorithm will use these binary keys for comparison.

    * This transparently wraps `PyICU`'s `collator.getSortKey(text)`.

  *  **`compare(self, a: str, b: str) -> int`:**

    * Explicitly compares two strings, returning -1, 0, or 1. Wraps `collator.compare(a, b)`.

  *  **Configuration (Builder Pattern):**

    * The `locale.get_collator()` method will accept optional arguments for common configurations. For advanced customization, a builder-style API could be considered for future extension to avoid the complexity of raw ICU rule strings.

 _Example Usage:_

Python

    
        import uicu
    locale = uicu.Locale('sv-SE') # Swedish
    collator = locale.get_collator()
    data = ['ångström', 'apple', 'zebra']
    # The collator object is used directly as the key
    sorted_data = sorted(data, key=collator)
    # Expected: ['apple', 'zebra', 'ångström']
    

### 2.5 The `uicu.format` Sub-package: Intuitive Data Formatting

This sub-package contains a suite of classes, each dedicated to a specific
formatting task.

 **`uicu.format.DateTimeFormatter`:**

  *  **Instantiation:** Via `locale.get_datetime_formatter(date_style: str = 'medium', time_style: str = 'medium', pattern: str = None, timezone: Union[str, datetime.tzinfo] = None)`.

    * `date_style` / `time_style` accept strings: `'full'`, `'long'`, `'medium'`, `'short'`, `'none'`. This replaces `icu.DateFormat.kDefault`, `LONG`, etc..

    * `pattern` allows for custom format strings (e.g., `'yyyy-MM-dd'`).

    * `timezone` accepts a timezone ID string (e.g., `'Europe/Berlin'`) or a `datetime.tzinfo` object.

  *  **`format(self, dt: datetime.datetime) -> str`:** Accepts a standard Python `datetime` object and returns a formatted string.

 **`uicu.format.NumberFormatter`:**

  *  **Instantiation:** Via `locale.get_number_formatter(style: str = 'decimal', pattern: str = None, min_fraction_digits: int = None,...)`

    * `style` accepts strings: `'decimal'`, `'percent'`, `'currency'`, `'scientific'`.

  *  **`format(self, number: Union) -> str`:** Formats a number.

  *  **`format_currency(self, number: Union, currency: str) -> str`:** A dedicated method for currency formatting that takes a 3-letter ISO 4217 currency code (e.g., `'USD'`, `'EUR'`).

 **`uicu.format.ListFormatter`:**

  *  **Instantiation:** Via `locale.get_list_formatter(style: str = 'standard', list_type: str = 'and')`.

    * `list_type` accepts `'and'`, `'or'`, or `'units'`.

  *  **`format(self, items: Iterable[str]) -> str`:** Joins an iterable of strings. _Example Usage:_ `locale.get_list_formatter().format(['one', 'two', 'three'])` -> `'one, two, and three'` (in English).

 **`uicu.format.MessageFormatter`:**

  *  **Instantiation:** Via `locale.get_message_formatter(pattern: str)`.

  *  **`format(self, **kwargs) -> str` or `format(params: Dict[str, Any]) -> str`:** Formats the message using ICU's rich plural and select rule syntax. _Example Usage:_

Python

    
        pattern = "{count, plural, one{# apple} other{# apples}} for {gender, select, male{him} female{her} other{them}}."
    msg_fmt = uicu.Locale('en').get_message_formatter(pattern)
    result = msg_fmt.format(count=1, gender='female')
    # result -> '1 apple for her'
    

### 2.6 The `uicu.segment` Module: Natural Text Segmentation

This module provides pythonic iterators for text boundary analysis, completely
abstracting the stateful `BreakIterator`.

 **`GraphemeSegmenter`, `WordSegmenter`, `SentenceSegmenter` Classes:**

  *  **Instantiation:** Via factory methods on a `Locale` object (e.g., `locale.get_word_segmenter()`). The segmenters are lightweight and can be created on-the-fly.

  *  **`segment(self, text: str) -> Iterator[str]`:**

    * This is the primary method for all segmenter classes. It takes a string and returns a generator that yields the segmented parts of the string.

    * This design allows for efficient, lazy processing of large texts and fits perfectly with Python's iteration patterns.

 _Example Usage:_

Python

    
        import uicu
    text = "The quick brown fox. It jumped."
    segmenter = uicu.Locale('en').get_sentence_segmenter()
    sentences = list(segmenter.segment(text))
    # sentences ->
    
    word_segmenter = uicu.Locale('en').get_word_segmenter()
    words = [word for word in word_segmenter.segment(text) if word.strip()]
    # words ->
    

### 2.7 The `uicu.translit` Module: Simplified Transliteration

This module provides a clean, functional interface for ICU's transliteration
capabilities.

  *  **`transliterate(text: str, transform_id: str) -> str`**

    * A high-level convenience function for one-off transformations. It creates, uses, and discards a `Transliterator` object internally.

    * `transform_id` is a string like `'Greek-Latin'` or `'Any-Hex'`. A list of available IDs can be retrieved via another function, `get_available_ids()`.

    * Raises `uicu.TransliterationError` if the `transform_id` is invalid.

  *  **`get_transliterator(transform_id: str, reverse: bool = False) -> Callable[[str], str]`**

    * A factory function for performance-sensitive applications where the same transformation is applied many times.

    * It pre-compiles the transliteration rule set by calling `icu.Transliterator.createInstance` and returns a simple, highly-optimized callable object (e.g., a function or a callable class instance).

    * This separates the expensive setup cost from the repeated application cost.

 _Example Usage:_

Python

    
        import uicu
    
    # Simple, one-off usage
    latin = uicu.translit.transliterate('Ψάπφω', 'Greek-Latin')
    # latin -> 'Psápphō'
    
    # Performant, repeated usage
    greek_to_latin = uicu.translit.get_transliterator('Greek-Latin')
    names = ['Σωκράτης', 'Πλάτων', 'Ἀριστοτέλης']
    latin_names = [greek_to_latin(name) for name in names]
    

## Part 3: Implementation and Documentation Roadmap

A successful library is more than just its code; it is the sum of its
implementation quality, documentation, and testing infrastructure. This
section provides a roadmap for building `uicu` into a robust, maintainable,
and user-friendly package.

### 3.1 Project Scaffolding and Dependencies

The project will be structured according to modern Python packaging best
practices to ensure compatibility with standard development and deployment
tools.

  *  **Directory Structure:**
    
        uicu/
    ├── docs/              # Sphinx documentation source
    ├── src/
    │   └── uicu/          # Main package source code
    │       ├── __init__.py
    │       ├── char.py
    │       ├── collate.py
    │       ├── locale.py
    │       ├── segment.py
    │       ├── translit.py
    │       └── format/
    │           ├── __init__.py
    │           └──...
    ├── tests/             # Pytest test suite
    ├── LICENSE
    ├── pyproject.toml     # Project metadata and build configuration
    └── README.md
    

  * **`pyproject.toml` Configuration:** This file is the single source of truth for project metadata and build dependencies. A minimal configuration would be:

Ini, TOML

    
        [project]
    name = "uicu"
    version = "0.1.0"
    description = "A pythonic, high-level wrapper for PyICU."
    readme = "README.md"
    requires-python = ">=3.8"
    license = { text = "MIT" }
    authors = [
        { name = "Your Name", email = "your@email.com" }
    ]
    classifiers =
    dependencies = [
        "pyicu >= 2.10",
        "fonttools[unicode] >= 4.40.0"
    ]
    
    [project.urls]
    Homepage = "https://github.com/user/uicu"
    Documentation = "https://uicu.readthedocs.io"
    Repository = "https://github.com/user/uicu"
    
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    

The critical line is `fonttools[unicode] >= 4.40.0`. The `[unicode]` extra
ensures that the `unicodedata2` dependency is installed, providing the up-to-
date Unicode data that is central to the library's design.

### 3.2 A Culture of Documentation and Testing

For a wrapper library like `uicu`, where the primary value proposition is an
improved developer experience, documentation is not an afterthought—it is a
core feature. The opaque and C++-centric nature of `PyICU`'s documentation is
a major usability obstacle. `uicu` must provide a comprehensive, python-first
documentation experience.

  *  **API Documentation:** Every public class, method, and function must have a comprehensive docstring following a standard format like Google Style or reST. This enables tools like Sphinx to automatically generate a professional API reference. Each docstring must include:

    * A one-line summary.

    * A more detailed explanation of its behavior.

    * Descriptions for all arguments (`Args:`).

    * A description of the return value (`Returns:`).

    * Any exceptions that may be raised (`Raises:`).

    * A simple, runnable code example (`Example:`).

  *  **User-Facing Documentation (to be built with Sphinx):** The documentation should be structured into four distinct categories, following the Diátaxis framework:

    1.  **Tutorials / Quickstart:** A "Getting Started" guide that begins with a consolidated, best-practice guide for installing `PyICU` and its dependencies, drawing from the scattered advice found online. It will then walk the user through a compelling, end-to-end example, such as sorting a list of Swedish names and formatting a date for a German locale.

    2.  **How-To Guides:** Topic-specific, goal-oriented recipes. The most important of these will be a guide titled **"From`PyICU` to `uicu`"**. This document will explicitly show "before" (`PyICU`) and "after" (`uicu`) code for common tasks, directly addressing the anti-patterns identified in Part 1. This provides a clear migration path and immediately demonstrates the library's value to existing `PyICU` users.

    3.  **Explanation / Discussion:** Conceptual articles that explain the "why" behind `uicu`'s design. This will include a page on the "Data Authority Principle," explaining the hybrid use of `PyICU` and `fontTools.unicodedata` and the rationale for it.

    4.  **API Reference:** The complete, auto-generated reference from the code's docstrings.

  *  **Testing Strategy (to be implemented with Pytest):** A rigorous test suite is non-negotiable for ensuring the correctness and stability of the wrapper.

    *  **Unit Tests:** Each module in `uicu` should have corresponding unit tests that mock the underlying `PyICU` and `fontTools` calls. These tests will verify that the wrapper logic (e.g., argument handling, type conversion, method delegation) is correct in isolation.

    *  **Integration Tests:** A suite of tests that use the real `PyICU` and `fontTools` libraries to verify end-to-end functionality. These tests should cover a representative set of locales (e.g., a LTR language like German, a RTL language like Arabic, a CJK language like Japanese) and use cases to ensure the abstractions behave as expected.

    *  **Exception Tests:** Tests must be written to confirm that the correct `uicu` exceptions are raised under specific failure conditions (e.g., passing an invalid locale to `uicu.Locale` should raise `uicu.ConfigurationError`).

    *  **Test Coverage:** The project should aim for high test coverage (e.g., >95%) and use tools to track it, ensuring that all logic paths are exercised.

Sources used in the report

[![](https://t3.gstatic.com/faviconV2?url=https://fonttools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)fonttools.readthedocs.iounicodedata:
Interface to character and script data in Unicode and ... Opens in a new
window
](https://fonttools.readthedocs.io/en/latest/unicodedata/index.html)[![](https://t0.gstatic.com/faviconV2?url=https://unicode-
org.github.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)unicode-
org.github.ioICU 77.1: Main Page Opens in a new window ](https://unicode-
org.github.io/icu-
docs/apidoc/dev/icu4c/)[![](https://t1.gstatic.com/faviconV2?url=https://gitee.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitee.comopenKylin/pyicu
- Gitee Opens in a new window ](https://gitee.com/openkylin/pyicu)

Sources read but not used in the report

[![](https://t3.gstatic.com/faviconV2?url=https://www.bedrick.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)bedrick.orgPython's
ICU Bindings - Steven Bedrick Opens in a new window
](https://www.bedrick.org/notes/python-icu-
bindings/)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comREADME.md
- ovalhub/pyicu - GitHub Opens in a new window
](https://github.com/ovalhub/pyicu/blob/master/README.md)[![](https://t0.gstatic.com/faviconV2?url=https://gitlab.pyicu.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitlab.pyicu.orgsamples
· main · main / pyicu · GitLab Opens in a new window
](https://gitlab.pyicu.org/main/pyicu/-/tree/main/samples)[![](https://t3.gstatic.com/faviconV2?url=https://www.freshports.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)freshports.orgFreshPorts
-- devel/py-pyicu: Python extension wrapping the ICU C++ API Opens in a new
window ](https://www.freshports.org/devel/py-
pyicu/)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.compyicu/CHANGES
at master - GitHub Opens in a new window
](https://github.com/ovalhub/pyicu/blob/master/CHANGES)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to correctly install PyICU on Heroku? - Stack Overflow Opens in a new window
](https://stackoverflow.com/questions/67646388/how-to-correctly-install-pyicu-
on-
heroku)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comInstall
Pyicu in python 3.x - Stack Overflow Opens in a new window
](https://stackoverflow.com/questions/46871401/install-pyicu-in-
python-3-x)[![](https://t1.gstatic.com/faviconV2?url=https://llego.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)llego.devAPI
Design and Testing in Python Technical Interviews - llego.dev Opens in a new
window ](https://llego.dev/posts/api-design-testing-python-technical-
interviews/)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)dev.toA
Pythonic Guide to SOLID Design Principles - DEV Community Opens in a new
window ](https://dev.to/ezzy1337/a-pythonic-guide-to-solid-design-
principles-4c8i)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgpyicu
- PyPI Opens in a new window
](https://pypi.org/project/pyicu/)[![](https://t2.gstatic.com/faviconV2?url=https://roguelynn.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)roguelynn.comDesign
of Everyday APIs · roguelynn - Lynn Root Opens in a new window
](https://roguelynn.com/words/everyday-
apis/)[![](https://t2.gstatic.com/faviconV2?url=https://www.pypistats.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypistats.orgpyicu
- PyPI Download Stats Opens in a new window
](https://www.pypistats.org/packages/pyicu)[![](https://t3.gstatic.com/faviconV2?url=https://realpython.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)realpython.comReal
Python: Python Tutorials Opens in a new window
](https://realpython.com/)[![](https://t0.gstatic.com/faviconV2?url=https://gitlab.pyicu.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitlab.pyicu.orgcommon.cpp
- main / pyicu · GitLab Opens in a new window
](https://gitlab.pyicu.org/main/pyicu/-/blob/main/common.cpp?ref_type=heads)[![](https://t3.gstatic.com/faviconV2?url=https://anaconda.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)anaconda.orgPyicu
- Anaconda.org Opens in a new window ](https://anaconda.org/conda-
forge/pyicu)[![](https://t1.gstatic.com/faviconV2?url=https://www.piwheels.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)piwheels.orgPyICU-
binary - piwheels Opens in a new window
](https://www.piwheels.org/project/pyicu-
binary/)[![](https://t0.gstatic.com/faviconV2?url=https://gist.github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gist.github.comInstallation
instructions for libicu-dev, PyICU, libpostal, pypostal on Mac OS X - GitHub
Gist Opens in a new window
](https://gist.github.com/ddelange/6e04e81b99fae08e817a00515d4a378d)[![](https://t3.gstatic.com/faviconV2?url=https://realpython.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)realpython.comPython
and REST APIs: Interacting With Web Services Opens in a new window
](https://realpython.com/api-integration-in-
python/)[![](https://t3.gstatic.com/faviconV2?url=https://hajloo.wordpress.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)hajloo.wordpress.comHow
to Use FontTools Module in Python | Hadjloo's Daily Notes - WordPress.com
Opens in a new window ](https://hajloo.wordpress.com/2011/07/15/how-to-use-
fonttools-module-in-
python/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comPip
can't install pyicu - Stack Overflow Opens in a new window
](https://stackoverflow.com/questions/68349833/pip-cant-install-
pyicu)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comarrowtype/fonttools-
intro: An introduction to FontTools & font development - GitHub Opens in a new
window ](https://github.com/arrowtype/fonttools-
intro)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comfonttools/fonttools:
A library to manipulate font files from Python. - GitHub Opens in a new window
](https://github.com/fonttools/fonttools)[![](https://t0.gstatic.com/faviconV2?url=https://docs.unity3d.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.unity3d.comOptimize
font files with font subsetting - Unity - Manual Opens in a new window
](https://docs.unity3d.com/6000.2/Documentation/Manual/UIE-font-
subsetting.html)[![](https://t2.gstatic.com/faviconV2?url=https://markoskon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)markoskon.comCreating
font subsets - Dev Diary Opens in a new window
](https://markoskon.com/creating-font-
subsets/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to use fontTools to detect Type 1 and OpenType CFF fonts - Stack Overflow
Opens in a new window ](https://stackoverflow.com/questions/55966692/how-to-
use-fonttools-to-detect-type-1-and-opentype-cff-
fonts)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgfonttools
- PyPI Opens in a new window
](https://pypi.org/project/fonttools/4.51.0/)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgfonttools
- PyPI Opens in a new window
](https://pypi.org/project/fonttools/)[![](https://t3.gstatic.com/faviconV2?url=https://fonttools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)fonttools.readthedocs.io—fontTools
Documentation— — fontTools Documentation Opens in a new window
](https://fonttools.readthedocs.io/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to use pyftsubset of Fonttools inside of the python environment, not from the
command line - Stack Overflow Opens in a new window
](https://stackoverflow.com/questions/55009981/how-to-use-pyftsubset-of-
fonttools-inside-of-the-python-environment-not-from-
th)[![](https://t0.gstatic.com/faviconV2?url=https://gist.github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gist.github.comPyICU
cheat sheet · GitHub Opens in a new window
](https://gist.github.com/dpk/8325992)[![](https://t0.gstatic.com/faviconV2?url=https://retailtechinnovationhub.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)retailtechinnovationhub.comThe
ultimate guide to structuring a Python package - Retail Technology Innovation
Hub Opens in a new window
](https://retailtechinnovationhub.com/home/2024/2/29/the-ultimate-guide-to-
structuring-a-python-
package)[![](https://t0.gstatic.com/faviconV2?url=https://help.autodesk.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)help.autodesk.comPython
API Best Practices - Autodesk Help Opens in a new window
](https://help.autodesk.com/view/SGDEV/ENU/?guid=SGD_py_python_api_best_practices_html)[![](https://t1.gstatic.com/faviconV2?url=https://nsls-
ii.github.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)nsls-
ii.github.ioGuiding Design Principles — Scientific Python Cookiecutter 0.1
documentation Opens in a new window ](https://nsls-ii.github.io/scientific-
python-cookiecutter/guiding-design-
principles.html)[![](https://t3.gstatic.com/faviconV2?url=https://docs.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.python.orgunicodedata
— Unicode Database — Python 3.13.5 documentation Opens in a new window
](https://docs.python.org/3/library/unicodedata.html)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)dev.toMastering
REST API Best Practices in Python - DEV Community Opens in a new window
](https://dev.to/biswajitfsd/mastering-rest-api-best-practices-in-
python-5bda)[![](https://t0.gstatic.com/faviconV2?url=https://www.stuartellis.name/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stuartellis.nameModern
Good Practices for Python Development - Stuart Ellis Opens in a new window
](https://www.stuartellis.name/articles/python-modern-
practices/)[![](https://t3.gstatic.com/faviconV2?url=https://www.freshports.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)freshports.orgFreshPorts
-- devel/py-unicodedata2: Unicodedata backport updated to the latest Unicode
version Opens in a new window ](https://www.freshports.org/devel/py-
unicodedata2)[![](https://t2.gstatic.com/faviconV2?url=https://stackoverflow.blog/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.blogBest
practices for REST API design - The Stack Overflow Blog Opens in a new window
](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-
design/)[![](https://t2.gstatic.com/faviconV2?url=https://docs.python-
guide.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.python-
guide.orgStructuring Your Project - The Hitchhiker's Guide to Python Opens in
a new window ](https://docs.python-
guide.org/writing/structure/)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgunicodedata2
- PyPI Opens in a new window
](https://pypi.org/project/unicodedata2/)[![](https://t3.gstatic.com/faviconV2?url=https://peps.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)peps.python.orgPEP
8 – Style Guide for Python Code | peps.python.org Opens in a new window
](https://peps.python.org/pep-0008/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.compython:
how to add 'unicodedata' module to my current python lib - Stack Overflow
Opens in a new window ](https://stackoverflow.com/questions/26583944/python-
how-to-add-unicodedata-module-to-my-current-python-
lib)[![](https://t3.gstatic.com/faviconV2?url=https://salishsea-meopar-
tools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)salishsea-
meopar-tools.readthedocs.ioGuidelines and Best Practices for Writing Library
Code Opens in a new window ](https://salishsea-meopar-
tools.readthedocs.io/en/latest/python_packaging/library_code.html)[![](https://t1.gstatic.com/faviconV2?url=https://prefix.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)prefix.devunicodedata2
- conda-forge - prefix.dev Opens in a new window
](https://prefix.dev/channels/conda-
forge/packages/unicodedata2)[![](https://t2.gstatic.com/faviconV2?url=https://benhoyt.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)benhoyt.comDesigning
Pythonic library APIs - Ben Hoyt Opens in a new window
](https://benhoyt.com/writings/python-api-
design/)[![](https://t3.gstatic.com/faviconV2?url=https://anaconda.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)anaconda.orgConda
- Anaconda.org Opens in a new window ](https://anaconda.org/conda-
forge/unicodedata2/)[![](https://t2.gstatic.com/faviconV2?url=https://packaging.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)packaging.python.orgPackaging
Python Projects Opens in a new window
](https://packaging.python.org/tutorials/packaging-projects/)

Thoughts

Understanding the Goal

I'm starting a new research task to design a Python library called `uicu`.
This library will serve as a more intuitive and Pythonic wrapper around
`PyICU`, with additional capabilities from `fontTools.unicodedata`. My main
goal is to create a detailed specification for this new library, making it
easy for a junior developer to implement.

Initial Research Approach

My first step is to thoroughly understand the existing APIs of both `PyICU`
and `fontTools.unicodedata`. I'll be looking into their modules, classes, and
methods, paying close attention to areas where `PyICU` might be powerful but
less Pythonic. I'll also investigate how `fontTools.unicodedata` handles
script and property information, and how it compares to Python's standard
`unicodedata` module.

Next Steps in Planning

After understanding the existing libraries, I'll compare their features to
identify overlaps and unique functionalities, which will guide decisions on
how to integrate them into `uicu`. I'll also research best practices for
Python API design to ensure `uicu` is truly Pythonic. Finally, I'll outline
the modular structure, define core objects, and plan for seamless integration
with Python's built-in string types, performance considerations,
documentation, and error handling. I'm beginning by gathering all relevant
documentation for both libraries.

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

Researching websites

[![](https://t3.gstatic.com/faviconV2?url=https://www.bedrick.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)bedrick.orgPython's
ICU Bindings - Steven Bedrick](https://www.bedrick.org/notes/python-icu-
bindings/)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comREADME.md
- ovalhub/pyicu -
GitHub](https://github.com/ovalhub/pyicu/blob/master/README.md)[![](https://t0.gstatic.com/faviconV2?url=https://unicode-
org.github.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)unicode-
org.github.ioICU 77.1: Main Page](https://unicode-org.github.io/icu-
docs/apidoc/dev/icu4c/)[![](https://t0.gstatic.com/faviconV2?url=https://gitlab.pyicu.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitlab.pyicu.orgsamples
· main · main / pyicu ·
GitLab](https://gitlab.pyicu.org/main/pyicu/-/tree/main/samples)[![](https://t3.gstatic.com/faviconV2?url=https://www.freshports.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)freshports.orgFreshPorts
-- devel/py-pyicu: Python extension wrapping the ICU C++
API](https://www.freshports.org/devel/py-
pyicu/)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.compyicu/CHANGES
at master -
GitHub](https://github.com/ovalhub/pyicu/blob/master/CHANGES)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to correctly install PyICU on Heroku? - Stack
Overflow](https://stackoverflow.com/questions/67646388/how-to-correctly-
install-pyicu-on-
heroku)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comInstall
Pyicu in python 3.x - Stack
Overflow](https://stackoverflow.com/questions/46871401/install-pyicu-in-
python-3-x)[![](https://t0.gstatic.com/faviconV2?url=https://gist.github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gist.github.comPyICU
cheat sheet - Gist -
GitHub](https://gist.github.com/dpk/8325992)[![](https://t1.gstatic.com/faviconV2?url=https://llego.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)llego.devAPI
Design and Testing in Python Technical Interviews -
llego.dev](https://llego.dev/posts/api-design-testing-python-technical-
interviews/)[![](https://t1.gstatic.com/faviconV2?url=https://gitee.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitee.comopenKylin/pyicu
-
Gitee](https://gitee.com/openkylin/pyicu)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)dev.toA
Pythonic Guide to SOLID Design Principles - DEV
Community](https://dev.to/ezzy1337/a-pythonic-guide-to-solid-design-
principles-4c8i)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgpyicu
-
PyPI](https://pypi.org/project/pyicu/)[![](https://t2.gstatic.com/faviconV2?url=https://roguelynn.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)roguelynn.comDesign
of Everyday APIs · roguelynn - Lynn
Root](https://roguelynn.com/words/everyday-
apis/)[![](https://t2.gstatic.com/faviconV2?url=https://www.pypistats.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypistats.orgpyicu
- PyPI Download
Stats](https://www.pypistats.org/packages/pyicu)[![](https://t3.gstatic.com/faviconV2?url=https://realpython.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)realpython.comReal
Python: Python
Tutorials](https://realpython.com/)[![](https://t0.gstatic.com/faviconV2?url=https://gitlab.pyicu.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitlab.pyicu.orgcommon.cpp
- main / pyicu ·
GitLab](https://gitlab.pyicu.org/main/pyicu/-/blob/main/common.cpp?ref_type=heads)[![](https://t3.gstatic.com/faviconV2?url=https://anaconda.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)anaconda.orgPyicu
- Anaconda.org](https://anaconda.org/conda-
forge/pyicu)[![](https://t1.gstatic.com/faviconV2?url=https://www.piwheels.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)piwheels.orgPyICU-
binary - piwheels](https://www.piwheels.org/project/pyicu-
binary/)[![](https://t0.gstatic.com/faviconV2?url=https://gist.github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gist.github.comInstallation
instructions for libicu-dev, PyICU, libpostal, pypostal on Mac OS X - GitHub
Gist](https://gist.github.com/ddelange/6e04e81b99fae08e817a00515d4a378d)[![](https://t3.gstatic.com/faviconV2?url=https://realpython.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)realpython.comPython
and REST APIs: Interacting With Web Services](https://realpython.com/api-
integration-in-
python/)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)dev.toMastering
REST API Best Practices in Python - DEV
Community](https://dev.to/biswajitfsd/mastering-rest-api-best-practices-in-
python-5bda)[![](https://t2.gstatic.com/faviconV2?url=https://benhoyt.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)benhoyt.comDesigning
Pythonic library APIs - Ben Hoyt](https://benhoyt.com/writings/python-api-
design/)[![](https://t3.gstatic.com/faviconV2?url=https://hajloo.wordpress.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)hajloo.wordpress.comHow
to Use FontTools Module in Python | Hadjloo's Daily Notes -
WordPress.com](https://hajloo.wordpress.com/2011/07/15/how-to-use-fonttools-
module-in-
python/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comPip
can't install pyicu - Stack
Overflow](https://stackoverflow.com/questions/68349833/pip-cant-install-
pyicu)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comarrowtype/fonttools-
intro: An introduction to FontTools & font development -
GitHub](https://github.com/arrowtype/fonttools-
intro)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)github.comfonttools/fonttools:
A library to manipulate font files from Python. -
GitHub](https://github.com/fonttools/fonttools)[![](https://t0.gstatic.com/faviconV2?url=https://docs.unity3d.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.unity3d.comOptimize
font files with font subsetting - Unity -
Manual](https://docs.unity3d.com/6000.2/Documentation/Manual/UIE-font-
subsetting.html)[![](https://t2.gstatic.com/faviconV2?url=https://markoskon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)markoskon.comCreating
font subsets - Dev Diary](https://markoskon.com/creating-font-
subsets/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to use fontTools to detect Type 1 and OpenType CFF fonts - Stack
Overflow](https://stackoverflow.com/questions/55966692/how-to-use-fonttools-
to-detect-type-1-and-opentype-cff-
fonts)[![](https://t3.gstatic.com/faviconV2?url=https://docs.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.python.orgunicodedata
— Unicode Database — Python 3.13.5
documentation](https://docs.python.org/3/library/unicodedata.html)[![](https://t3.gstatic.com/faviconV2?url=https://fonttools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)fonttools.readthedocs.iounicodedata:
Interface to character and script data in Unicode and
OpenType](https://fonttools.readthedocs.io/en/latest/unicodedata/index.html)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgfonttools
-
PyPI](https://pypi.org/project/fonttools/4.51.0/)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgfonttools
-
PyPI](https://pypi.org/project/fonttools/)[![](https://t3.gstatic.com/faviconV2?url=https://fonttools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)fonttools.readthedocs.io—fontTools
Documentation— — fontTools
Documentation](https://fonttools.readthedocs.io/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.comHow
to use pyftsubset of Fonttools inside of the python environment, not from the
command line - Stack
Overflow](https://stackoverflow.com/questions/55009981/how-to-use-pyftsubset-
of-fonttools-inside-of-the-python-environment-not-from-th)

Initial API Exploration

I've started by gathering information on PyICU and fontTools.unicodedata. For
PyICU, I've found a cheat sheet and official documentation that provide
insights into its core functionalities like transliteration, locale handling,
collation, date formatting, and break iteration. A key observation is that
PyICU often requires explicit `UnicodeString` objects and in-place
modifications, which is less Pythonic than working with native Python strings.
However, it also offers 'Pythonic' ways for some operations, like
`locale.getDisplayName()` returning a Python `str` directly. For
`fontTools.unicodedata`, the documentation highlights its role in accessing
Unicode character properties, script data, and OpenType script tags,
complementing the standard `unicodedata` module with more up-to-date and
specialized data.

Addressing Pythonic Design

I'm also looking into general principles for designing Pythonic APIs. Key
themes emerging include prioritizing intuitive and consistent naming, keeping
APIs simple and minimal, minimizing interdependencies between components
(loose coupling), and supporting versioning. The importance of clear
documentation, comprehensive testing (unit, integration, usability, load), and
effective error handling is also being emphasized. I'm noting examples of both
good and less ideal API designs within the Python standard library to inform
the `uicu` design.

Next Steps in Research

My next step is to delve deeper into the specifics of PyICU and
`fontTools.unicodedata` by browsing the identified key documentation. I'll
focus on understanding the nuances of their APIs, particularly the areas where
PyICU deviates from Pythonic conventions, to inform how `uicu` can bridge
these gaps. I'll also continue to synthesize information on Pythonic API
design to ensure the `uicu` library is both extensive and natural to use.

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

Researching websites

[![](https://t0.gstatic.com/faviconV2?url=https://gist.github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gist.github.comPyICU
cheat sheet ·
GitHub](https://gist.github.com/dpk/8325992)[![](https://t3.gstatic.com/faviconV2?url=https://fonttools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)fonttools.readthedocs.iounicodedata:
Interface to character and script data in Unicode and
...](https://fonttools.readthedocs.io/en/latest/unicodedata/index.html)[![](https://t0.gstatic.com/faviconV2?url=https://unicode-
org.github.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)unicode-
org.github.ioICU 77.1: Main Page](https://unicode-org.github.io/icu-
docs/apidoc/dev/icu4c/)[![](https://t1.gstatic.com/faviconV2?url=https://gitee.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)gitee.comopenKylin/pyicu
- Gitee](https://gitee.com/openkylin/pyicu)

Deepening API Understanding

I've gained a clearer understanding of PyICU's API, confirming its direct
mapping to the ICU4C C++ library. This means it often uses mutable
`UnicodeString` objects and in-place modifications, which are less aligned
with Python's immutable string philosophy. I've also identified its reliance
on factory methods and verbose naming conventions. In contrast,
`fontTools.unicodedata` provides specialized Unicode character properties,
script, and OpenType-related information, building upon an updated Unicode
database, which complements Python's built-in `unicodedata` module.

Identifying Design Challenges

A significant challenge for `uicu` will be to abstract away PyICU's non-
Pythonic elements while retaining its powerful functionality. This involves
designing an API that feels natural to Python developers, potentially by
converting mutable `UnicodeString` objects to Python's native immutable
strings where appropriate, and by adopting more idiomatic Python patterns for
object creation and method calls. I'm also considering how to best integrate
the unique capabilities of `fontTools.unicodedata` to provide a comprehensive
and user-friendly experience.

Charting the Path Forward

My immediate next steps involve a detailed feature comparison between PyICU
and `fontTools.unicodedata` to pinpoint overlaps and unique strengths.
Concurrently, I'll synthesize the gathered Pythonic API design principles into
concrete goals for `uicu`. This will then lead to outlining the `uicu` package
structure, defining its core objects, and considering how to manage
performance and integrate seamlessly with Python's native types. I'll also
plan for robust documentation and a custom exception hierarchy.

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

Researching websites

[![](https://t0.gstatic.com/faviconV2?url=https://retailtechinnovationhub.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)retailtechinnovationhub.comThe
ultimate guide to structuring a Python package - Retail Technology Innovation
Hub](https://retailtechinnovationhub.com/home/2024/2/29/the-ultimate-guide-to-
structuring-a-python-
package)[![](https://t0.gstatic.com/faviconV2?url=https://help.autodesk.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)help.autodesk.comPython
API Best Practices - Autodesk
Help](https://help.autodesk.com/view/SGDEV/ENU/?guid=SGD_py_python_api_best_practices_html)[![](https://t1.gstatic.com/faviconV2?url=https://nsls-
ii.github.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)nsls-
ii.github.ioGuiding Design Principles — Scientific Python Cookiecutter 0.1
documentation](https://nsls-ii.github.io/scientific-python-
cookiecutter/guiding-design-
principles.html)[![](https://t3.gstatic.com/faviconV2?url=https://docs.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.python.orgunicodedata
— Unicode Database — Python 3.13.5
documentation](https://docs.python.org/3/library/unicodedata.html)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)dev.toMastering
REST API Best Practices in Python - DEV
Community](https://dev.to/biswajitfsd/mastering-rest-api-best-practices-in-
python-5bda)[![](https://t0.gstatic.com/faviconV2?url=https://www.stuartellis.name/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stuartellis.nameModern
Good Practices for Python Development - Stuart
Ellis](https://www.stuartellis.name/articles/python-modern-
practices/)[![](https://t3.gstatic.com/faviconV2?url=https://www.freshports.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)freshports.orgFreshPorts
-- devel/py-unicodedata2: Unicodedata backport updated to the latest Unicode
version](https://www.freshports.org/devel/py-
unicodedata2)[![](https://t2.gstatic.com/faviconV2?url=https://stackoverflow.blog/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.blogBest
practices for REST API design - The Stack Overflow
Blog](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-
design/)[![](https://t2.gstatic.com/faviconV2?url=https://docs.python-
guide.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)docs.python-
guide.orgStructuring Your Project - The Hitchhiker's Guide to
Python](https://docs.python-
guide.org/writing/structure/)[![](https://t1.gstatic.com/faviconV2?url=https://pypi.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)pypi.orgunicodedata2
-
PyPI](https://pypi.org/project/unicodedata2/)[![](https://t3.gstatic.com/faviconV2?url=https://peps.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)peps.python.orgPEP
8 – Style Guide for Python Code |
peps.python.org](https://peps.python.org/pep-0008/)[![](https://t0.gstatic.com/faviconV2?url=https://stackoverflow.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)stackoverflow.compython:
how to add 'unicodedata' module to my current python lib - Stack
Overflow](https://stackoverflow.com/questions/26583944/python-how-to-add-
unicodedata-module-to-my-current-python-
lib)[![](https://t3.gstatic.com/faviconV2?url=https://salishsea-meopar-
tools.readthedocs.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)salishsea-
meopar-tools.readthedocs.ioGuidelines and Best Practices for Writing Library
Code](https://salishsea-meopar-
tools.readthedocs.io/en/latest/python_packaging/library_code.html)[![](https://t1.gstatic.com/faviconV2?url=https://prefix.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)prefix.devunicodedata2
- conda-forge - prefix.dev](https://prefix.dev/channels/conda-
forge/packages/unicodedata2)[![](https://t2.gstatic.com/faviconV2?url=https://benhoyt.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)benhoyt.comDesigning
Pythonic library APIs - Ben Hoyt](https://benhoyt.com/writings/python-api-
design/)[![](https://t3.gstatic.com/faviconV2?url=https://anaconda.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)anaconda.orgConda
- Anaconda.org](https://anaconda.org/conda-
forge/unicodedata2/)[![](https://t2.gstatic.com/faviconV2?url=https://packaging.python.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)packaging.python.orgPackaging
Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

Synthesizing Research Findings

I have completed my research into PyICU and `fontTools.unicodedata`, and have
a solid understanding of their APIs, strengths, and areas where a more
Pythonic approach is needed. I've also thoroughly explored Pythonic API design
principles, which will be crucial in shaping the `uicu` library. I'm now ready
to synthesize all this information into a detailed specification.

Preparing the `uicu` Specification

My next action is to generate a comprehensive report that will serve as the
detailed specification for the `uicu` package. This report will guide a junior
developer in implementing the library, ensuring it is extensive, natural, and
performant, while seamlessly integrating with Python's native Unicode
capabilities and exposing rich additional functionality.

