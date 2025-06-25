#!/usr/bin/env python
# this_file: src/uicu/exceptions.py
"""Exception hierarchy for the uicu package.

This module defines custom exceptions for clear and specific error handling
throughout the uicu package.
"""


class UICUError(Exception):
    """Base exception for all uicu errors."""

    pass


class ConfigurationError(UICUError):
    """Invalid configuration (locale, pattern, etc.)."""

    pass


class FormattingError(UICUError):
    """Error during formatting operations."""

    pass


class CollationError(UICUError):
    """Error in collation operations."""

    pass


class SegmentationError(UICUError):
    """Error in text segmentation."""

    pass


class TransliterationError(UICUError):
    """Error in transliteration."""

    pass
