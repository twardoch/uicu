#!/usr/bin/env python
from __future__ import annotations

# this_file: src/uicu/exceptions.py
"""Exception hierarchy for the uicu package."""


class UICUError(Exception):
    """Base exception for all uicu errors."""

    pass


class ConfigurationError(UICUError):
    """Invalid configuration (locale, pattern, etc.)."""

    pass


class OperationError(UICUError):
    """Error during runtime operations (formatting, collation, etc.)."""

    pass
