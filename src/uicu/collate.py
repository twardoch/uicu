#!/usr/bin/env python
# this_file: src/uicu/collate.py
"""Locale-aware string comparison and sorting.

This module provides Pythonic interfaces for ICU's collation functionality,
enabling locale-sensitive string comparison and sorting.
"""

from collections.abc import Iterable

import icu

from uicu._utils import ensure_locale
from uicu.exceptions import ConfigurationError
from uicu.locale import Locale

# Map string strength names to ICU constants
STRENGTH_MAP = {
    "primary": icu.Collator.PRIMARY,
    "secondary": icu.Collator.SECONDARY,
    "tertiary": icu.Collator.TERTIARY,
    "quaternary": icu.Collator.QUATERNARY,
    "identical": icu.Collator.IDENTICAL,
}


class Collator:
    """Locale-aware string collator for sorting.

    This class wraps ICU's Collator to provide locale-sensitive string
    comparison and sorting. It can be used directly as a key function
    with Python's sorted() function.
    """

    def __init__(
        self,
        locale: str | Locale,
        strength: str = "tertiary",
        *,
        numeric: bool = False,
        case_first: str | None = None,
        case_level: bool = False,
    ):
        """Create a collator.

        Args:
            locale: Locale identifier string or Locale object.
            strength: Comparison strength level:
                     - 'primary': Base letters only (ignore case, accents)
                     - 'secondary': Consider accents (ignore case)
                     - 'tertiary': Consider case differences (default)
                     - 'quaternary': Consider variant differences
                     - 'identical': Bit-for-bit identical
            numeric: Enable numeric sorting where "2" < "10".
            case_first: Which case to sort first - 'upper', 'lower', or None.
            case_level: Enable separate case level between secondary and tertiary.

        Raises:
            ConfigurationError: If locale or configuration is invalid.
        """
        # Convert string locale to Locale object if needed
        locale = ensure_locale(locale)

        # Create ICU collator
        self._collator = icu.Collator.createInstance(locale._icu_locale)

        # Set strength
        if strength not in STRENGTH_MAP:
            msg = f"Invalid strength '{strength}'. Must be one of: {', '.join(STRENGTH_MAP.keys())}"
            raise ConfigurationError(msg)
        self._collator.setStrength(STRENGTH_MAP[strength])

        # Configure numeric sorting
        if numeric:
            self._collator.setAttribute(icu.UCollAttribute.NUMERIC_COLLATION, icu.UCollAttributeValue.ON)

        # Configure case ordering
        if case_first == "upper":
            self._collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.UPPER_FIRST)
        elif case_first == "lower":
            self._collator.setAttribute(icu.UCollAttribute.CASE_FIRST, icu.UCollAttributeValue.LOWER_FIRST)

        # Configure case level
        if case_level:
            self._collator.setAttribute(icu.UCollAttribute.CASE_LEVEL, icu.UCollAttributeValue.ON)

        # Store configuration for reference
        self._locale = locale
        self._strength = strength
        self._numeric = numeric

    def compare(self, a: str, b: str) -> int:
        """Compare two strings according to collation rules.

        Returns -1 if a < b, 0 if a == b, 1 if a > b.
        """
        result = self._collator.compare(a, b)
        # Normalize to -1, 0, 1
        if result < 0:
            return -1
        if result > 0:
            return 1
        return 0

    def key(self, s: str) -> bytes:
        """Return sort key for string.

        The sort key is a byte sequence that, when compared using
        standard byte comparison, yields the same ordering as would
        be obtained using the collator's compare method.

        Args:
            s: String to create sort key for.

        Returns:
            Sort key as bytes.
        """
        # getSortKey returns bytes directly in PyICU
        return self._collator.getSortKey(s)

    def __call__(self, s: str) -> bytes:
        """Make collator callable as a key function.

        This allows using the collator directly with sorted():
        sorted(strings, key=collator)

        Args:
            s: String to create sort key for.

        Returns:
            Sort key as bytes.
        """
        return self.key(s)

    def sort(self, strings: Iterable[str]) -> list[str]:
        """Return sorted copy of strings.

        Args:
            strings: Iterable of strings to sort.

        Returns:
            New list with strings sorted according to collation rules.
        """
        return sorted(strings, key=self.key)

    def is_equal(self, a: str, b: str) -> bool:
        """Check if two strings are equal according to collation rules.

        Args:
            a: First string.
            b: Second string.

        Returns:
            True if strings are considered equal.
        """
        return self.compare(a, b) == 0

    def is_less(self, a: str, b: str) -> bool:
        """Check if first string is less than second.

        Args:
            a: First string.
            b: Second string.

        Returns:
            True if a < b according to collation rules.
        """
        return self.compare(a, b) < 0

    def is_greater(self, a: str, b: str) -> bool:
        """Check if first string is greater than second.

        Args:
            a: First string.
            b: Second string.

        Returns:
            True if a > b according to collation rules.
        """
        return self.compare(a, b) > 0

    @property
    def locale(self) -> Locale:
        """The locale this collator is configured for."""
        return self._locale

    @property
    def strength(self) -> str:
        """The configured strength level."""
        return self._strength

    @property
    def numeric(self) -> bool:
        """Whether numeric sorting is enabled."""
        return self._numeric

    def __repr__(self) -> str:
        """Return a representation of the collator."""
        return f"Collator(locale='{self._locale.language_tag}', strength='{self._strength}', numeric={self._numeric})"


# Convenience functions


def sort(strings: Iterable[str], locale: str | Locale, **options) -> list[str]:
    """Sort strings according to locale rules.

    This is a convenience function that creates a temporary collator
    for one-off sorting operations.

    Args:
        strings: Iterable of strings to sort.
        locale: Locale identifier or Locale object.
        **options: Additional options passed to Collator constructor.

    Returns:
        New list with strings sorted according to locale rules.

    Example:
        >>> sort(['café', 'cote', 'côte', 'coté'], 'fr-FR')
        ['café', 'cote', 'coté', 'côte']
    """
    collator = Collator(locale, **options)
    return collator.sort(strings)


def compare(a: str, b: str, locale: str | Locale, **options) -> int:
    """Compare two strings according to locale rules.

    This is a convenience function that creates a temporary collator
    for one-off comparisons.

    Args:
        a: First string.
        b: Second string.
        locale: Locale identifier or Locale object.
        **options: Additional options passed to Collator constructor.

    Returns:
        -1 if a < b, 0 if a == b, 1 if a > b.
    """
    collator = Collator(locale, **options)
    return collator.compare(a, b)
