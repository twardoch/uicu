Below is a detailed specification document for the new **`uicu`** package. This spec outlines design goals, module and API structure, integration strategies, error handling, testing guidelines, and documentation conventions. It is written so that a junior developer can follow it step by step to develop the package.

---

# uicu Package Specification

The **`uicu`** package is intended to be a comprehensive, natural, and pythonic API for ICU functionality. It serves as a wrapper around [PyICU](https://pypi.org/project/pyicu/) and supplements any necessary APIs from [fontTools.unicodedata](https://fonttools.readthedocs.io/en/latest/unicodedata/index.html) or the updated [unicodedata2](https://github.com/fonttools/unicodedata2) project. The package will provide rich objects that naturally integrate with Python’s native Unicode types while exposing advanced and performant ICU operations.

---

## 1. Overview and Goals

- **Primary Goal:**  
  Build a pythonic and extensive API for ICU functionality that seamlessly wraps PyICU. The API aims to simplify and enhance the standard ICU features (localization, date and time formatting, Unicode normalization, and more) in a way that leverages Python’s strengths.

- **Key Objectives:**
  - **Pythonic Interface:** Hide low-level ICU details (such as error-code handling and non-native string types) behind a natural interface that works well with Python’s native types.
  - **Rich Typing:** Provide well-documented objects and methods for locales, text formats, time zones, and Unicode data.
  - **Performance:** Wrap the PyICU (C++ based) backend so that performance remains a priority.
  - **Extensibility:** Offer integration points to supplement ICU functionality with advanced Unicode lookup (using fontTools.unicodedata, unicodedata2, or even Python’s builtin unicodedata where applicable).
  - **Error Simplification:** Automatically manage ICU error codes and exceptions by translating them into standard Python exceptions.

---

## 2. Dependencies

- **PyICU:**  
  This is the underlying binding to the ICU C++ API.  
  > *Installation:* `pip install pyicu`

- **FontTools.unicodedata (or unicodedata2):**  
  To provide extra Unicode character data and support for writing systems, fall back on fontTools’ functionalities where needed.

- **Optional:**  
  Python’s built-in [unicodedata](https://docs.python.org/3/library/unicodedata.html) module for additional compatibility utilities.

---

## 3. Package Architecture and Module Layout

To keep the code maintainable, organize **`uicu`** into several modules:

- **`uicu/core.py`:**  
  Core implementations and helpers – low-level wrappers around PyICU objects, type conversions, and common utilities.

- **`uicu/locale.py`:**  
  Provides a pythonic `Locale` class which wraps ICU’s Locale. Include methods that convert ICU data (e.g. display names) into native Python strings.

- **`uicu/formatting.py`:**  
  Contains wrappers for ICU’s date/time formatting APIs. Offers classes like `DateFormat` with methods that accept Python numbers and `datetime` objects.

- **`uicu/unicode.py`:**  
  Provides Unicode-related functionalities, including normalization, lookup, and other text processing utilities:
  - A `UnicodeString` class that mimics a Python string while wrapping ICU’s mutable `UnicodeString`.
  - Functions such as `normalize(form, unistr)`, mirroring ICU’s normalization forms (NFC, NFKC, NFD, NFKD).

- **`uicu/timezone.py`:**  
  Implements time zone related helpers, including a wrapper type (`ICUtzinfo`) that implements Python’s `tzinfo` interface by wrapping ICU’s TimeZone object.

- **`uicu/errors.py`:**  
  Defines exception classes (e.g. `UICUError`) that wrap ICU errors. All errors from lower-level ICU calls will be caught and re-raised as these exceptions.

- **`uicu/data.py`:**  
  Optional module to integrate extra Unicode data (e.g. via fontTools.unicodedata) for enhanced support of writing systems, property lookups, and extended normalization if needed.

- **`uicu/utils.py`:**  
  Utilities for common tasks (e.g. caching lookups, conversion helpers between ICU and Python types).

---

## 4. API Design and Object Specifications

Below is an outline of the key objects and functions exposed by **`uicu`**:

### 4.1. Exceptions

- **`uicu.errors.UICUError(Exception)`**  
  - Base exception for all errors in the package.
  - Wraps ICU error codes and messages.

### 4.2. Locale

- **`uicu.locale.Locale`**
  - **Constructor:**  
    `Locale(identifier: str) → Locale`  
    Uses ICU’s locale constructor. The identifier can be in the form `"en_US"`, `"pt_BR"`, etc.
  - **Methods/Properties:**
    - `get_display_name() -> str`: Returns the locale’s display name using ICU under the hood.
    - `language: str`: Property to get the ISO language.
    - `country: str`: Property to get the country code.
    - `variant: Optional[str]`: If applicable.
  - **Examples:**
    ```python
    from uicu.locale import Locale

    loc = Locale("pt_BR")
    print(loc.get_display_name())  # "Portuguese (Brazil)"
    print(loc.language)  # "pt"
    ```

### 4.3. UnicodeString

- **`uicu.unicode.UnicodeString`**
  - **Description:**  
    A wrapper around ICU’s mutable `UnicodeString` that behaves similar to Python’s native string. Internally it will accept Python `str` in its constructors.
  - **Constructor:**  
    `UnicodeString(s: Union[str, ICU_UnicodeString]= "")`
  - **Methods/Operators:**
    - `__str__() -> str`: Converts the UnicodeString to a native Python string.
    - `__getitem__() and __setitem__()`: Provide slicing and indexing (note that slicing might return a new UnicodeString, as ICU slicing conventions differ).
    - `__iadd__()`: Support for in-place concatenation (`+=`).
    - Additional helper methods: `.to_upper()`, `.to_lower()`, etc.
  - **Usage Example:**
    ```python
    from uicu.unicode import UnicodeString

    ustr = UnicodeString("Café")
    print(str(ustr))  # "Café"
    ustr += " au lait"
    print(ustr)  # "Café au lait"
    ```

### 4.4. Normalization Functions

- **`uicu.unicode.normalize(form: str, unistr: Union[str, UnicodeString]) -> str`**
  - **Supported Forms:** `'NFC'`, `'NFD'`, `'NFKC'`, `'NFKD'`.
  - **Behavior:**  
    Converts the input (either a Python `str` or a `UnicodeString`) into the specified normalized form, utilizing ICU’s normalization functionality.
  - **Example:**
    ```python
    from uicu.unicode import normalize

    normalized = normalize("NFC", "Café")
    print(normalized)
    ```

- **`uicu.unicode.is_normalized(form: str, unistr: Union[str, UnicodeString]) -> bool`**  
  Returns whether a given string is in the specified normalized form.

### 4.5. Date and Time Formatting

- **`uicu.formatting.DateFormat`**
  - **Factory Method(s):**
    - `create_instance(locale: Union[str, Locale] = None) -> DateFormat`
      - Creates a date/time formatter instance. If no locale is provided, use the default.
  - **Methods:**
    - `format(date_value: Union[float, int, datetime, Formattable]) -> str`
      - Accepts numeric values, Python’s `datetime` objects, or ICU-specific Formattable objects. It automatically converts between Python’s time conventions (seconds since epoch) and ICU’s milliseconds.
    - `parse(text: str) -> datetime`
      - Converts formatted date strings back to Python’s `datetime`.
  - **Example:**
    ```python
    from uicu.formatting import DateFormat
    from datetime import datetime

    df = DateFormat.create_instance("en_US")
    now = datetime.now()
    formatted = df.format(now)
    print(formatted)   # e.g., "10/18/23 3:04 PM"
    parsed_date = df.parse(formatted)
    ```

### 4.6. Time Zone Handling

- **`uicu.timezone.ICUtzinfo`**
  - **Purpose:**  
    Provide a class that wraps ICU’s TimeZone and implements Python’s `tzinfo` interface.
  - **Class Methods:**
    - `get_instance(tz_id: str) -> ICUtzinfo`: Returns an instance for the given time zone identifier.
    - `get_default() -> ICUtzinfo`: Returns the system default time zone.
  - **Usage:**
    ```python
    from datetime import datetime
    from uicu.timezone import ICUtzinfo

    tz = ICUtzinfo.get_instance("Pacific/Fiji")
    now = datetime.now(tz)
    print(now)
    ```

### 4.7. Unicode Data / Character Properties

- **`uicu.data.UnicodeData`**
  - **Methods:**
    - `lookup(name: str) -> str`: Look up a Unicode character by its name.
    - `name(char: str, default: Optional[str] = None) -> str`: Return the Unicode name for the given character.
    - `category(char: str) -> str`: Return the general category.
    - `digit(char: str, default: Optional[int]=None) -> int`
    - `decimal(char: str, default: Optional[int]=None) -> int`
    - `numeric(char: str, default: Optional[float]=None) -> float`
  - **Integration Strategy:**  
    This module can either simply proxy calls to Python’s built-in `unicodedata`–or use the more up-to-date fontTools.unicodedata2 as needed. It should provide a single, unified API.

---

## 5. Design Patterns and Conventions

- **Type Coercion & Conversion:**  
  Every method that interacts with ICU’s native types should accept Python’s native types as input (e.g. Python `str` for text for Unicode functions, and Python’s `datetime` or numbers for date/time). Internally, conversion happens so that the PyICU APIs’ requirements are met.

- **Error Handling:**  
  All ICU calls are wrapped in try…except constructs. Instead of dealing with ICU’s `UErrorCode` semantics, our helper functions catch these and raise clean, understandable (`UICUError`) exceptions.

- **Immutable versus Mutable:**  
  Decide clearly on mutable wrappers (e.g. for `UnicodeString`) vs immutable conversions. Document the behavior so that developers know if operations return new objects or modify in place.

- **Naming and Documentation:**  
  Use clear, Pythonic naming conventions. Every public class or function should have a docstring that explains its parameters, return values, and sample usage. Provide inline comments when wrapping lower-level interfaces.

- **Testing / Examples:**  
  For each module, create a corresponding file in a `tests/` directory. Include unit tests covering:
  - Correct conversion between ICU and Python types.
  - Error handling and exception propagation.
  - Cross-platform behavior (especially for timezone and locale handling).

---

## 6. Development and Packaging Guidelines

- **Source Control:**  
  Use Git. Organize commits by feature (Locale, Unicode, Formatting, etc.). Ensure each commit is small and passes tests.

- **Setup and Installation:**  
  - Use a `setup.py` (or the modern `pyproject.toml` and `setuptools` configuration) to declare dependencies (PyICU, fontTools.unicodedata2 if needed).
  - Include instructions in the README for obtaining and configuring ICU libraries on different systems (like PyICU’s guidelines).

- **Documentation:**  
  Write comprehensive documentation using Markdown and host it on ReadTheDocs. Use Sphinx with autodoc extensions to further generate API documentation from the docstrings.

- **Continuous Integration:**  
  Set up CI (for example, GitHub Actions) to run your test suite automatically on different Python versions and platforms.

---

## 7. Example Usage in an Application

Here is an example script demonstrating how a user would benefit from **`uicu`**:

```python
from datetime import datetime
from uicu.locale import Locale
from uicu.formatting import DateFormat
from uicu.unicode import UnicodeString, normalize
from uicu.timezone import ICUtzinfo
from uicu.data import UnicodeData

# Locale usage
locale = Locale("en_US")
print("Locale Display:", locale.get_display_name())

# DateFormat usage
df = DateFormat.create_instance(locale)
now = datetime.now(ICUtzinfo.get_instance("America/New_York"))
print("Formatted Date:", df.format(now))

# UnicodeString and normalization
ustr = UnicodeString("Café")
print("Original:", str(ustr))
print("Normalized NFC:", normalize("NFC", ustr))
ustr += " – Enjoy!"
print("Concatenated:", str(ustr))

# Unicode data lookup
try:
    char = UnicodeData.lookup("LEFT CURLY BRACKET")
    print("Lookup:", char)
except KeyError:
    print("Character not found")
```

---

## 8. Final Checklist

- [ ] **Define core abstractions** (Locale, UnicodeString, DateFormat, ICUtzinfo, UnicodeData) with clear API contracts.  
- [ ] **Implement type conversion helpers** in `uicu/core.py` and `uicu/utils.py`.  
- [ ] **Wrap ICU error codes** into a custom error (`UICUError` in `uicu/errors.py`).  
- [ ] **Integrate (if needed) fontTools.unicodedata** functions in `uicu/data.py` with fallbacks to Python’s `unicodedata`.  
- [ ] **Write unit tests** for every module (each function, method, and error condition).  
- [ ] **Document all public-facing interfaces** with examples and docstrings.  
- [ ] **Package the library** using setuptools/pyproject.toml and add a README with installation instructions and usage examples.  
- [ ] **Set up CI/CD integration** for automated testing across platforms and Python versions.

---

By following this detailed specification, you will create the **`uicu`** package—a highly usable, pythonic, and comprehensive interface to the powerful ICU libraries for Unicode and internationalization support.