#!/usr/bin/env python
# this_file: src/uicu/segment.py
# pyright: ignore
"""Text boundary analysis (graphemes, words, sentences).

This module provides Pythonic interfaces for ICU's break iteration functionality,
enabling text segmentation according to Unicode rules and locale conventions.
"""

from collections.abc import Iterator

import icu

from uicu.exceptions import SegmentationError
from uicu.locale import Locale


def _create_break_iterator(
    kind: str,
    locale: Locale | None = None,
) -> icu.BreakIterator:
    """Create a break iterator of the specified kind.

    Args:
        kind: Type of iterator - 'character', 'word', 'sentence', or 'line'.
        locale: Optional locale for locale-specific rules.

    Returns:
        Configured BreakIterator instance.

    Raises:
        SegmentationError: If creation fails.
    """
    # Get the ICU locale
    icu_locale = icu.Locale.getDefault() if locale is None else locale._icu_locale

    # Create the appropriate iterator
    try:
        if kind == "character":
            return icu.BreakIterator.createCharacterInstance(icu_locale)
        if kind == "word":
            return icu.BreakIterator.createWordInstance(icu_locale)
        if kind == "sentence":
            return icu.BreakIterator.createSentenceInstance(icu_locale)
        if kind == "line":
            return icu.BreakIterator.createLineInstance(icu_locale)
        msg = f"Unknown iterator kind: {kind}"
        raise ValueError(msg)
    except Exception as e:
        msg = f"Failed to create {kind} iterator: {e}"
        raise SegmentationError(msg) from e


def _iterate_breaks(
    text: str,
    break_iterator: icu.BreakIterator,
) -> Iterator[str]:
    """Iterate over text segments using a break iterator.

    This handles the UTF-16 index conversion issue by using ICU's
    UnicodeString internally.

    Args:
        text: Text to segment.
        break_iterator: Configured break iterator.

    Yields:
        Text segments as strings.
    """
    if not text:
        return

    # Convert to ICU UnicodeString to handle UTF-16 indices correctly
    utext = icu.UnicodeString(text)
    break_iterator.setText(utext)

    # Get break positions
    start = 0
    for end in break_iterator:
        if end == icu.BreakIterator.DONE:
            break
        # Extract segment using UnicodeString slicing
        segment = utext[start:end]
        # Convert to Python string
        yield str(segment)
        start = end


# Functional API


def graphemes(text: str, locale: str | Locale | None = None) -> Iterator[str]:
    """Iterate over grapheme clusters (user-perceived characters).

    A grapheme cluster is what users think of as a single character,
    which may be composed of multiple Unicode code points.

    Args:
        text: Text to segment into graphemes.
        locale: Optional locale for locale-specific rules.
                Can be a string identifier or Locale object.

    Yields:
        Grapheme clusters as strings.

    Example:
        >>> list(graphemes('🇨🇦'))
        ['🇨🇦']  # Single flag emoji
        >>> list(graphemes('e\\u0301'))
        ['é']  # Combined character
        >>> list(graphemes('नमस्ते'))  # Devanagari
        ['न', 'म', 'स्', 'ते']  # Note combined characters
    """
    # Convert string locale to Locale object if needed
    if isinstance(locale, str):
        locale = Locale(locale)

    # Create character (grapheme) break iterator
    break_iterator = _create_break_iterator("character", locale)

    # Iterate over grapheme clusters
    yield from _iterate_breaks(text, break_iterator)


def words(
    text: str,
    locale: str | Locale | None = None,
    *,
    skip_whitespace: bool = True,
    skip_punctuation: bool = True,
) -> Iterator[str]:
    """Iterate over words according to locale rules.

    Word boundaries are determined by Unicode rules and may be
    customized by locale. Note that by default, whitespace and
    punctuation are skipped.

    Args:
        text: Text to segment into words.
        locale: Optional locale for locale-specific rules.
        skip_whitespace: If True, skip whitespace-only tokens.
        skip_punctuation: If True, skip punctuation-only tokens.

    Yields:
        Word tokens as strings.

    Example:
        >>> list(words("Hello, world!"))
        ['Hello', 'world']
        >>> list(words("你好世界", locale='zh-CN'))
        ['你好', '世界']  # Chinese word segmentation
    """
    # Convert string locale to Locale object if needed
    if isinstance(locale, str):
        locale = Locale(locale)

    # Create word break iterator
    break_iterator = _create_break_iterator("word", locale)

    # Iterate over words
    for word in _iterate_breaks(text, break_iterator):
        if skip_whitespace and word.isspace():
            continue
        if skip_punctuation and all(not c.isalnum() for c in word):
            continue
        yield word


def sentences(text: str, locale: str | Locale | None = None) -> Iterator[str]:
    """Iterate over sentences according to locale rules.

    Sentence boundaries are determined by Unicode rules and may be
    customized by locale. The sentences include their terminating
    punctuation.

    Args:
        text: Text to segment into sentences.
        locale: Optional locale for locale-specific rules.

    Yields:
        Sentences as strings.

    Example:
        >>> list(sentences("Hello. How are you? I'm fine!"))
        ['Hello. ', 'How are you? ', "I'm fine!"]
    """
    # Convert string locale to Locale object if needed
    if isinstance(locale, str):
        locale = Locale(locale)

    # Create sentence break iterator
    break_iterator = _create_break_iterator("sentence", locale)

    # Iterate over sentences
    yield from _iterate_breaks(text, break_iterator)


def lines(text: str, locale: str | Locale | None = None) -> Iterator[str]:
    """Iterate over line break opportunities.

    This identifies positions where lines can be broken for text
    wrapping according to Unicode rules.

    Args:
        text: Text to find line breaks in.
        locale: Optional locale for locale-specific rules.

    Yields:
        Text segments between line break opportunities.
    """
    # Convert string locale to Locale object if needed
    if isinstance(locale, str):
        locale = Locale(locale)

    # Create line break iterator
    break_iterator = _create_break_iterator("line", locale)

    # Iterate over line segments
    yield from _iterate_breaks(text, break_iterator)


def line_breaks(text: str, locale: str | Locale | None = None) -> Iterator[int]:
    """Find potential line break positions in text.

    This function returns the character positions (indices) where
    line breaks are allowed according to Unicode line breaking rules.

    Args:
        text: Text to analyze for line breaks.
        locale: Optional locale for locale-specific rules.

    Yields:
        Character positions where line breaks are allowed.
    """
    # Convert string locale to Locale object if needed
    if isinstance(locale, str):
        locale = Locale(locale)

    # Create line break iterator
    break_iterator = _create_break_iterator("line", locale)

    # Set text
    uset = icu.UnicodeString(text)
    break_iterator.setText(uset)

    # Get all boundaries
    position = break_iterator.first()
    while position != icu.BreakIterator.DONE:
        # Convert from UTF-16 to Python string position
        utf16_pos = position
        if utf16_pos > 0 and utf16_pos < len(uset):
            # Calculate Python string position
            python_pos = len(str(uset[:utf16_pos]))
            yield python_pos
        position = break_iterator.nextBoundary()


# OOP Interface


class BaseSegmenter:
    """Base class for text segmenters."""

    def __init__(self, locale: str | Locale | None = None):
        """Initialize segmenter with optional locale.

        Args:
            locale: Optional locale for locale-specific rules.
        """
        if isinstance(locale, str):
            locale = Locale(locale)
        self._locale = locale
        self._break_iterator = self._create_break_iterator()

    def _create_break_iterator(self) -> icu.BreakIterator:
        """Create the break iterator. Subclasses must implement."""
        raise NotImplementedError

    def segment(self, text: str) -> Iterator[str]:
        """Segment text into parts.

        Args:
            text: Text to segment.

        Yields:
            Text segments.
        """
        yield from _iterate_breaks(text, self._break_iterator)

    def segment_list(self, text: str) -> list[str]:
        """Segment text into a list.

        Args:
            text: Text to segment.

        Returns:
            List of text segments.
        """
        return list(self.segment(text))
    
    def boundaries(self, text: str) -> set[int]:
        """Get boundary positions in text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Set of boundary positions (character indices).
        """
        # Set text
        uset = icu.UnicodeString(text)
        self._break_iterator.setText(uset)
        
        # Collect all boundaries
        boundaries = set()
        position = self._break_iterator.first()
        while position != icu.BreakIterator.DONE:
            # Convert from UTF-16 to Python string position
            if position == 0:
                boundaries.add(0)
            elif position >= len(uset):
                boundaries.add(len(text))
            else:
                # Calculate Python string position
                python_pos = len(str(uset[:position]))
                boundaries.add(python_pos)
            position = self._break_iterator.nextBoundary()
        
        return boundaries


class GraphemeSegmenter(BaseSegmenter):
    """Reusable grapheme cluster segmenter."""

    def _create_break_iterator(self) -> icu.BreakIterator:
        """Create character break iterator."""
        return _create_break_iterator("character", self._locale)

    def __repr__(self) -> str:
        """Return representation."""
        locale_str = self._locale.language_tag if self._locale else "default"
        return f"GraphemeSegmenter(locale='{locale_str}')"


class WordSegmenter(BaseSegmenter):
    """Reusable word segmenter."""

    def __init__(
        self,
        locale: str | Locale | None = None,
        *,
        skip_whitespace: bool = False,
    ):
        """Initialize word segmenter.

        Args:
            locale: Optional locale for locale-specific rules.
            skip_whitespace: If True, skip whitespace tokens.
        """
        super().__init__(locale)
        self._skip_whitespace = skip_whitespace

    def _create_break_iterator(self) -> icu.BreakIterator:
        """Create word break iterator."""
        return _create_break_iterator("word", self._locale)

    def segment(self, text: str) -> Iterator[str]:
        """Segment text into words.

        Args:
            text: Text to segment.

        Yields:
            Word tokens.
        """
        for word in super().segment(text):
            if self._skip_whitespace and word.isspace():
                continue
            yield word

    def __repr__(self) -> str:
        """Return representation."""
        locale_str = self._locale.language_tag if self._locale else "default"
        return f"WordSegmenter(locale='{locale_str}', skip_whitespace={self._skip_whitespace})"


class SentenceSegmenter(BaseSegmenter):
    """Reusable sentence segmenter."""

    def _create_break_iterator(self) -> icu.BreakIterator:
        """Create sentence break iterator."""
        return _create_break_iterator("sentence", self._locale)

    def __repr__(self) -> str:
        """Return representation."""
        locale_str = self._locale.language_tag if self._locale else "default"
        return f"SentenceSegmenter(locale='{locale_str}')"


class LineSegmenter(BaseSegmenter):
    """Reusable line break segmenter."""

    def _create_break_iterator(self) -> icu.BreakIterator:
        """Create line break iterator."""
        return _create_break_iterator("line", self._locale)

    def __repr__(self) -> str:
        """Return representation."""
        locale_str = self._locale.language_tag if self._locale else "default"
        return f"LineSegmenter(locale='{locale_str}')"
