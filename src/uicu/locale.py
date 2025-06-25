#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING

import icu

from uicu.exceptions import ConfigurationError

# Type hints for forward references
if TYPE_CHECKING:
    from uicu.collate import Collator
    from uicu.format import DateTimeFormatter
    from uicu.segment import (
        GraphemeSegmenter,
        SentenceSegmenter,
        WordSegmenter,
    )

# this_file: src/uicu/locale.py
"""Locale management and factory for locale-aware services.

This module provides the central Locale class that represents a specific locale
and serves as a factory for creating locale-aware services like collators,
formatters, and segmenters.
"""


class Locale:
    """Represents a specific locale and creates locale-aware services.

    This class wraps ICU's Locale functionality and provides factory methods
    for creating various locale-aware services.
    """

    def __init__(self, language_tag: str):
        """Initialize a locale.

        Args:
            language_tag: BCP 47 language tag (e.g. 'en-US', 'fr-FR')

        Raises:
            ConfigurationError: If locale creation fails
        """
        try:
            self._icu_locale = icu.Locale(language_tag)
        except Exception as e:
            msg = f"Failed to create locale for '{language_tag}': {e}"
            raise ConfigurationError(msg) from e

        self._language_tag = language_tag

        # Cache commonly accessed properties
        self._language = self._icu_locale.getLanguage()
        self._script = self._icu_locale.getScript()
        self._country = self._icu_locale.getCountry()  # ICU uses "country" for region
        self._variant = self._icu_locale.getVariant()

    @property
    def display_name(self) -> str:
        """Full human-readable name in default locale.

        Returns:
            Display name like 'English (United Kingdom)'.
        """
        # Get display name in the default locale
        return self._icu_locale.getDisplayName()

    def get_display_name_in_locale(self, display_locale: Locale | None = None) -> str:
        """Get display name in a specific locale.

        Args:
            display_locale: Locale to use for display. If None, uses default.

        Returns:
            Display name in the specified locale.
        """
        if display_locale is None:
            return self.display_name
        return self._icu_locale.getDisplayName(display_locale._icu_locale)

    @property
    def language(self) -> str:
        """ISO 639 language code.

        Returns:
            Two or three letter language code (e.g., 'en', 'zh').
        """
        return self._language

    @property
    def script(self) -> str:
        """ISO 15924 script code if specified.

        Returns:
            Four-letter script code (e.g., 'Latn', 'Hant') or empty string.
        """
        return self._script

    @property
    def region(self) -> str:
        """ISO 3166 region code.

        Returns:
            Two-letter region code (e.g., 'GB', 'US') or empty string.
        """
        return self._country

    @property
    def variant(self) -> str:
        """Variant code or empty string."""
        return self._variant

    @property
    def base_name(self) -> str:
        """The canonical locale identifier (e.g., 'en_GB', 'zh_Hant_TW')."""
        return self._icu_locale.getBaseName()

    @property
    def language_tag(self) -> str:
        """BCP 47 language tag.

        Returns:
            Language tag with hyphens (e.g., 'en-GB', 'zh-Hant-TW').
        """
        return self.base_name.replace("_", "-")

    # Factory methods for locale-aware services

    def get_collator(self, strength: str = "tertiary", *, numeric: bool = False, **kwargs) -> Collator:
        """Create a collator for this locale.

        Args:
            strength: The collation strength level. One of:
                - "primary" - Base characters only
                - "secondary" - Base + accents
                - "tertiary" - Base + accents + case (default)
                - "quaternary" - Base + accents + case + punctuation
            numeric: Whether to use numeric collation
            **kwargs: Additional collation options

        Returns:
            A collator for this locale
        """
        from uicu.collate import Collator

        return Collator(self, strength=strength, numeric=numeric, **kwargs)

    def get_datetime_formatter(
        self,
        date_style: str = "medium",
        time_style: str = "medium",
        **kwargs,
    ) -> DateTimeFormatter:
        """Create a date/time formatter for this locale.

        Args:
            date_style: Date format style ('none', 'short', 'medium', 'long', 'full')
            time_style: Time format style ('none', 'short', 'medium', 'long', 'full')
            **kwargs: Additional formatter options

        Returns:
            A date/time formatter for this locale
        """
        from uicu.format import DateTimeFormatter

        return DateTimeFormatter(
            self,
            date_style=date_style,
            time_style=time_style,
            **kwargs,
        )

    def get_date_formatter(
        self,
        style: str = "medium",
        **kwargs,
    ) -> DateTimeFormatter:
        """Create a date-only formatter for this locale.

        Args:
            style: Date format style ('short', 'medium', 'long', 'full')
            **kwargs: Additional formatter options

        Returns:
            A date-only formatter for this locale
        """
        return self.get_datetime_formatter(date_style=style, time_style="none", **kwargs)

    def get_time_formatter(
        self,
        style: str = "medium",
        **kwargs,
    ) -> DateTimeFormatter:
        """Create a time-only formatter for this locale.

        Args:
            style: Time format style ('short', 'medium', 'long', 'full')
            **kwargs: Additional formatter options

        Returns:
            A time-only formatter for this locale
        """
        return self.get_datetime_formatter(date_style="none", time_style=style, **kwargs)

    #
    # def get_number_formatter(
    #     self,
    #     style: str = "decimal",
    #     **kwargs,
    # ) -> "NumberFormatter":
    #     """Create a number formatter for this locale.
    #
    #     Args:
    #         style: Format style - 'decimal', 'percent', 'currency', 'scientific'.
    #         **kwargs: Additional options passed to NumberFormatter.
    #
    #     Returns:
    #         A configured NumberFormatter instance.
    #     """
    #     from uicu.format import NumberFormatter
    #
    #     return NumberFormatter(self, style=style, **kwargs)
    #
    # def get_list_formatter(
    #     self,
    #     style: str = "standard",
    #     list_type: str = "and",
    #     **kwargs,
    # ) -> "ListFormatter":
    #     """Create a list formatter for this locale.
    #
    #     Args:
    #         style: Format style - 'standard', 'narrow', etc.
    #         list_type: List type - 'and', 'or', 'units'.
    #         **kwargs: Additional options passed to ListFormatter.
    #
    #     Returns:
    #         A configured ListFormatter instance.
    #     """
    #     from uicu.format import ListFormatter
    #
    #     return ListFormatter(
    #         self,
    #         style=style,
    #         list_type=list_type,
    #         **kwargs,
    #     )

    def get_word_segmenter(self) -> WordSegmenter:
        """Create a word segmenter for this locale.

        Returns:
            A new WordSegmenter instance for this locale
        """
        # Import here to avoid circular imports
        from uicu.segment import WordSegmenter

        return WordSegmenter(self)

    def get_grapheme_segmenter(self) -> GraphemeSegmenter:
        """Create a grapheme segmenter for this locale.

        Returns:
            A new GraphemeSegmenter instance for this locale
        """
        # Import here to avoid circular imports
        from uicu.segment import GraphemeSegmenter

        return GraphemeSegmenter(self)

    def get_sentence_segmenter(self) -> SentenceSegmenter:
        """Create a sentence segmenter for this locale.

        Returns:
            A new SentenceSegmenter instance for this locale
        """
        # Import here to avoid circular imports
        from uicu.segment import SentenceSegmenter

        return SentenceSegmenter(self)

    def __str__(self) -> str:
        """Return the locale identifier."""
        return self.base_name

    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"Locale('{self.language_tag}')"

    def __eq__(self, other) -> bool:
        """Compare locales."""
        if isinstance(other, Locale):
            return self.base_name == other.base_name
        return NotImplemented

    def __hash__(self) -> int:
        """Hash based on base name."""
        return hash(self.base_name)


# Convenience functions


def get_available_locales() -> list[str]:
    """Get list of available locale identifiers.

    Returns:
        List of locale identifiers supported by ICU.
    """
    # Get all available locales from ICU
    locales = []
    for locale_id in icu.Locale.getAvailableLocales():
        if locale_id:  # Skip empty locale
            # getAvailableLocales returns strings
            locales.append(locale_id.replace("_", "-"))
    return sorted(locales)


def get_default_locale() -> Locale:
    """Get the system default locale.

    Returns:
        The default Locale instance.
    """
    default_icu = icu.Locale.getDefault()
    identifier = default_icu.getBaseName()
    return Locale(identifier)
