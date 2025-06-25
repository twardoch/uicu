#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uicu.locale import Locale

# this_file: src/uicu/_utils.py
"""Internal utilities for uicu package.

This module contains shared utility functions used internally by uicu modules.
These functions are private to the package and not part of the public API.
"""


def ensure_locale(locale: str | Locale) -> Locale:
    """Convert string to Locale object if needed.

    Args:
        locale: Either a Locale object or BCP 47 language tag string.

    Returns:
        Locale object.

    Raises:
        ICU errors if locale string is invalid.
    """
    # Use duck typing instead of isinstance to avoid circular imports
    if hasattr(locale, "language_tag"):
        return locale  # Already a Locale object

    # Import here is safe since we're in a utility module
    from uicu.locale import Locale

    return Locale(locale)
