#!/usr/bin/env python
# this_file: src/uicu/_utils.py
"""Internal utilities for uicu package.

This module contains shared utility functions used internally by uicu modules.
These functions are private to the package and not part of the public API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uicu.locale import Locale


def ensure_locale(locale: str | Locale) -> Locale:
    """Convert string to Locale object if needed.

    Args:
        locale: Either a Locale object or BCP 47 language tag string.

    Returns:
        Locale object.

    Raises:
        ICU errors if locale string is invalid.
    """
    if isinstance(locale, str):
        # Import here to avoid circular imports
        from uicu.locale import Locale

        return Locale(locale)
    return locale
