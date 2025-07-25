#!/usr/bin/env python
from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import icu

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


# Performance optimization: Cache expensive ICU object creation
@lru_cache(maxsize=128)
def _get_cached_collator(locale_id: str, strength: int, numeric: bool, case_level: bool) -> icu.Collator:
    """Cache expensive ICU collator creation.
    
    Args:
        locale_id: Locale identifier string
        strength: ICU collation strength constant
        numeric: Whether to use numeric collation
        case_level: Whether to use case level
        
    Returns:
        Cached ICU Collator instance
    """
    collator = icu.Collator.createInstance(icu.Locale(locale_id))
    collator.setStrength(strength)
    
    if numeric:
        collator.setAttribute(icu.UCollAttribute.NUMERIC_COLLATION, icu.UCollAttributeValue.ON)
    
    if case_level:
        collator.setAttribute(icu.UCollAttribute.CASE_LEVEL, icu.UCollAttributeValue.ON)
    
    return collator


@lru_cache(maxsize=64)
def _get_cached_transliterator(transform_id: str) -> icu.Transliterator:
    """Cache expensive ICU transliterator creation.
    
    Args:
        transform_id: Transliterator ID string
        
    Returns:
        Cached ICU Transliterator instance
    """
    return icu.Transliterator.createInstance(transform_id)


@lru_cache(maxsize=64)
def _get_cached_break_iterator(locale_id: str, iterator_type: str) -> icu.BreakIterator:
    """Cache expensive ICU break iterator creation.
    
    Args:
        locale_id: Locale identifier string
        iterator_type: Type of break iterator (word, sentence, etc.)
        
    Returns:
        Cached ICU BreakIterator instance
    """
    locale = icu.Locale(locale_id)
    
    if iterator_type == "grapheme":
        return icu.BreakIterator.createCharacterInstance(locale)
    elif iterator_type == "word":
        return icu.BreakIterator.createWordInstance(locale)
    elif iterator_type == "sentence":
        return icu.BreakIterator.createSentenceInstance(locale)
    elif iterator_type == "line":
        return icu.BreakIterator.createLineInstance(locale)
    else:
        raise ValueError(f"Unknown iterator type: {iterator_type}")
