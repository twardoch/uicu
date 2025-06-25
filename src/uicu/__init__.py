#!/usr/bin/env python
# this_file: src/uicu/__init__.py
"""uicu - A Pythonic wrapper for PyICU.

This package provides natural, Pythonic interfaces to ICU's powerful
internationalization and Unicode capabilities, making advanced text
processing accessible to Python developers.
"""

# Version information
try:
    from uicu._version import __version__  # type: ignore
except ImportError:
    __version__ = "0.0.1dev"

# Import main components for convenient access
from uicu.char import (
    # Classes
    Char,
    bidirectional,
    block,
    category,
    combining,
    decimal,
    digit,
    mirrored,
    # Functions
    name,
    numeric,
    script,
    script_direction,
    script_extensions,
    script_name,
)
from uicu.collate import Collator, compare, sort
from uicu.exceptions import (
    ConfigurationError,
    UICUError,
)
from uicu.locale import Locale, get_available_locales, get_default_locale
from uicu.segment import (
    # Classes
    GraphemeSegmenter,
    LineSegmenter,
    SentenceSegmenter,
    WordSegmenter,
    # Functions
    graphemes,
    line_breaks,
    lines,
    sentences,
    words,
)
from uicu.translit import (
    Transliterator,
    find_transforms,
    get_available_transforms,
    transliterate,
)

# Import formatting components
try:
    from uicu.format import DateTimeFormatter, ListFormatter, NumberFormatter
except ImportError:
    # Format module not yet fully implemented
    DateTimeFormatter = None
    ListFormatter = None
    NumberFormatter = None

# Import script detection dependencies at module level
try:
    from uicu.char import HAS_FONTTOOLS
    from uicu.char import script as get_script
except ImportError:
    HAS_FONTTOOLS = False
    get_script = None


# Script detection helper
def detect_script(text: str) -> str | None:
    """Detect the primary script used in text.

    Args:
        text: Text to analyze.

    Returns:
        ISO 15924 script code (e.g., 'Latn', 'Cyrl', 'Hani') or None if mixed.
    """
    if not text:
        return None

    try:
        if not HAS_FONTTOOLS or get_script is None:
            return None

        # Count scripts used
        script_counts = {}
        for char in text:
            if char.isalpha():  # Only count alphabetic characters
                s = get_script(char)
                if s not in ("Zyyy", "Zinh", "Zzzz"):  # Ignore common/inherited/unknown
                    script_counts[s] = script_counts.get(s, 0) + 1

        if not script_counts:
            return None

        # Return most common script
        return max(script_counts.items(), key=lambda x: x[1])[0]
    except Exception:
        return None


# Define what's exported with "from uicu import *"
__all__ = [
    "Char",
    "CollationError",
    "Collator",
    "ConfigurationError",
    "DateTimeFormatter",
    "FormattingError",
    "GraphemeSegmenter",
    "LineSegmenter",
    "ListFormatter",
    "Locale",
    "NumberFormatter",
    "SegmentationError",
    "SentenceSegmenter",
    "TransliterationError",
    "Transliterator",
    "UICUError",
    "WordSegmenter",
    "__version__",
    "bidirectional",
    "block",
    "category",
    "combining",
    "compare",
    "decimal",
    "detect_script",
    "digit",
    "find_transforms",
    "get_available_locales",
    "get_available_transforms",
    "get_default_locale",
    "graphemes",
    "line_breaks",
    "lines",
    "mirrored",
    "name",
    "numeric",
    "script",
    "script_direction",
    "script_extensions",
    "script_name",
    "sentences",
    "sort",
    "transliterate",
    "words",
]
