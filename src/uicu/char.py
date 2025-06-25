#!/usr/bin/env python
# this_file: src/uicu/char.py
"""Unicode character properties module.

This module provides Pythonic access to Unicode character information using
the latest Unicode data from fontTools.unicodedata with fallback to Python's
built-in unicodedata module.

Note: This module analyzes individual Unicode codepoints. Multi-codepoint
grapheme clusters (like flag emojis) should be broken into individual
codepoints for analysis. Use the uicu.segment module for grapheme-aware
text processing.
"""

import unicodedata
from typing import Any

try:
    from fontTools import unicodedata as ftunicodedata

    HAS_FONTTOOLS = True
except ImportError:
    HAS_FONTTOOLS = False
    import unicodedata as ftunicodedata
    import warnings

    warnings.warn(
        "fontTools.unicodedata not available. Using built-in unicodedata which may have older Unicode data.",
        ImportWarning,
        stacklevel=2,
    )


def _normalize_char_input(char: str | int) -> str:
    """Normalize character input to a single character string.
    
    Converts integer codepoints to characters and validates string length.
    """
    if isinstance(char, int):
        try:
            return chr(char)
        except ValueError as e:
            msg = f"Invalid codepoint: {char}"
            raise ValueError(msg) from e
    if isinstance(char, str):
        if len(char) != 1:
            # Check if it might be a multi-codepoint grapheme
            if len(char) > 1:
                msg = (
                    f"Expected single character, got string of length {len(char)}. "
                    f"Multi-codepoint sequences like '{char}' are not supported. "
                    f"Consider using char[0] to analyze the first codepoint, "
                    f"or use uicu.graphemes() for grapheme-aware processing."
                )
            else:
                msg = f"Expected single character, got empty string"
            raise ValueError(msg)
        return char

    msg = f"Expected str or int, got {type(char).__name__}"
    raise TypeError(msg)


# Basic properties (delegate to fontTools.unicodedata or built-in)


def name(char: str | int, default: str | None = None) -> str | None:
    """Return Unicode name of character.
    
    Returns default if character has no name, raises ValueError if no default.
    """
    char = _normalize_char_input(char)
    try:
        return ftunicodedata.name(char)
    except ValueError:
        if default is not None:
            return default
        raise


def category(char: str | int) -> str:
    """Return general category (e.g., 'Lu' for uppercase letter)."""
    char = _normalize_char_input(char)
    return ftunicodedata.category(char)


def bidirectional(char: str | int) -> str:
    """Return bidirectional class (e.g., 'L' for left-to-right)."""
    char = _normalize_char_input(char)
    return ftunicodedata.bidirectional(char)


def combining(char: str | int) -> int:
    """Return canonical combining class as integer."""
    char = _normalize_char_input(char)
    return ftunicodedata.combining(char)


def mirrored(char: str | int) -> bool:
    """Return True if character is mirrored in bidi text."""
    char = _normalize_char_input(char)
    # fontTools.unicodedata doesn't have mirrored property
    # Always use built-in unicodedata for this
    return bool(unicodedata.mirrored(char))


def decimal(char: str | int, default: Any = None) -> int | None:
    """Return decimal value of character, or default if none."""
    char = _normalize_char_input(char)
    try:
        return ftunicodedata.decimal(char)
    except (KeyError, ValueError):
        return default


def digit(char: str | int, default: Any = None) -> int | None:
    """Return digit value of character.

    Args:
        char: A single character or integer codepoint.
        default: Default value if character has no digit value.

    Returns:
        Digit value as integer, or default if provided.

    Raises:
        ValueError: If no digit value and no default provided.
    """
    char = _normalize_char_input(char)
    try:
        return ftunicodedata.digit(char)
    except (KeyError, ValueError):
        return default


def numeric(char: str | int, default: Any = None) -> int | float | None:
    """Return numeric value of character, or default if none."""
    char = _normalize_char_input(char)
    try:
        return ftunicodedata.numeric(char)
    except (KeyError, ValueError):
        return default


# Script and block properties (unique to fontTools)


def script(char: str | int) -> str:
    """Return ISO 15924 script code (e.g., 'Latn', 'Hani')."""
    if not HAS_FONTTOOLS:
        msg = "script() requires fontTools.unicodedata"
        raise NotImplementedError(msg)
    char = _normalize_char_input(char)
    return ftunicodedata.script(char)


def script_name(code: str) -> str:
    """Return human-readable script name for ISO 15924 code."""
    if not HAS_FONTTOOLS:
        msg = "script_name() requires fontTools.unicodedata"
        raise NotImplementedError(msg)
    return ftunicodedata.script_name(code)


def script_extensions(char: str | int) -> set[str]:
    """Return set of scripts that use this character."""
    if not HAS_FONTTOOLS:
        msg = "script_extensions() requires fontTools.unicodedata"
        raise NotImplementedError(msg)
    char = _normalize_char_input(char)
    # fontTools returns a set for script extensions
    extensions = ftunicodedata.script_extension(char)
    # If no extensions, return set with just the main script
    if not extensions:
        return {script(char)}
    return extensions


def block(char: str | int) -> str:
    """Return Unicode block name.

    Args:
        char: A single character or integer codepoint.

    Returns:
        Unicode block name (e.g., 'Basic Latin').
    """
    if not HAS_FONTTOOLS:
        msg = "block() requires fontTools.unicodedata"
        raise NotImplementedError(msg)
    char = _normalize_char_input(char)
    return ftunicodedata.block(char)


def script_direction(script_code: str) -> str:
    """Return 'LTR' or 'RTL' for script direction.

    Args:
        script_code: Four-letter ISO 15924 script code.

    Returns:
        'LTR' for left-to-right or 'RTL' for right-to-left.
    """
    if not HAS_FONTTOOLS:
        msg = "script_direction() requires fontTools.unicodedata"
        raise NotImplementedError(msg)
    return ftunicodedata.script_horizontal_direction(script_code)  # type: ignore[attr-defined]


# Optional OOP Interface


class Char:
    """Rich Unicode character object.

    This class provides an object-oriented interface to Unicode character
    properties, bundling all property access into a single object.
    
    Note: This class currently only supports single Unicode codepoints.
    Multi-codepoint grapheme clusters (like flag emojis 🇺🇸) are not
    supported. Use the first codepoint or iterate over the string to
    analyze individual codepoints.
    """

    def __init__(self, char: str | int):
        """Initialize with a character or codepoint.

        Args:
            char: A single character string or integer codepoint.
                  Multi-codepoint sequences like flag emojis are not supported.
                  
        Raises:
            ValueError: If char is a multi-character string.
        """
        self._char = _normalize_char_input(char)
        self._codepoint = ord(self._char)

    @property
    def char(self) -> str:
        """The character as a string."""
        return self._char

    @property
    def codepoint(self) -> int:
        """The Unicode codepoint as an integer."""
        return self._codepoint

    @property
    def name(self) -> str | None:
        """Unicode name of the character."""
        return name(self._char, f"U+{self._codepoint:04X}")

    @property
    def category(self) -> str:
        """General category code."""
        return category(self._char)

    @property
    def bidirectional(self) -> str:
        """Bidirectional class."""
        return bidirectional(self._char)

    @property
    def combining(self) -> int:
        """Canonical combining class."""
        return combining(self._char)

    @property
    def mirrored(self) -> bool:
        """True if character is mirrored in bidi text."""
        return mirrored(self._char)

    @property
    def decimal(self) -> int | None:
        """Decimal value or None."""
        return decimal(self._char, None)

    @property
    def digit(self) -> int | None:
        """Digit value or None."""
        return digit(self._char, None)

    @property
    def numeric(self) -> int | float | None:
        """Numeric value or None."""
        return numeric(self._char, None)

    @property
    def script(self) -> str | None:
        """ISO 15924 script code."""
        if not HAS_FONTTOOLS:
            return None
        return script(self._char)

    @property
    def script_extensions(self) -> set[str]:
        """Set of scripts that use this character."""
        if not HAS_FONTTOOLS:
            return set()
        return script_extensions(self._char)

    @property
    def block(self) -> str | None:
        """Unicode block name."""
        if not HAS_FONTTOOLS:
            return None
        return block(self._char)

    def __str__(self) -> str:
        """Return the character itself."""
        return self._char

    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"<Char {self._char!r} U+{self._codepoint:04X} '{self.name}'>"

    def __eq__(self, other: object) -> bool:
        """Compare characters."""
        if isinstance(other, Char):
            return self._char == other._char
        if isinstance(other, str):
            return self._char == other
        return NotImplemented

    def __hash__(self) -> int:
        """Hash based on the character."""
        return hash(self._char)
