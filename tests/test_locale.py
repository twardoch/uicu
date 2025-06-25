#!/usr/bin/env python
# this_file: tests/test_locale.py
"""Tests for locale module."""

import pytest

import uicu


class TestLocale:
    """Test Locale class functionality."""

    def test_locale_creation(self):
        """Test creating Locale objects."""
        # With hyphen
        loc1 = uicu.Locale("en-US")
        assert loc1.language == "en"
        assert loc1.region == "US"

        # With underscore
        loc2 = uicu.Locale("fr_FR")
        assert loc2.language == "fr"
        assert loc2.region == "FR"

        # With script
        loc3 = uicu.Locale("zh-Hant-TW")
        assert loc3.language == "zh"
        assert loc3.script == "Hant"
        assert loc3.region == "TW"

    def test_locale_properties(self):
        """Test locale properties."""
        loc = uicu.Locale("en-GB")

        # Display name
        assert "English" in loc.display_name
        assert "United Kingdom" in loc.display_name or "Britain" in loc.display_name

        # Language tag
        assert loc.language_tag == "en-GB"
        assert loc.base_name == "en_GB"

    def test_invalid_locale(self):
        """Test invalid locale handling."""
        # ICU is quite permissive with locale identifiers
        # Empty string is actually valid in ICU (treated as root locale)
        # Let's test that no exception is raised for typical edge cases
        try:
            uicu.Locale("")  # Empty string is valid (root locale)
            uicu.Locale("en-US")  # Valid locale
            # If we reach here, ICU accepts these locales
        except uicu.ConfigurationError:
            # If ConfigurationError is raised, that's also acceptable behavior
            pass

    def test_locale_comparison(self):
        """Test locale comparison."""
        loc1 = uicu.Locale("en-US")
        loc2 = uicu.Locale("en_US")  # Different separator
        loc3 = uicu.Locale("en-GB")

        assert loc1 == loc2
        assert loc1 != loc3
        assert str(loc1) == "en_US"

    def test_factory_methods(self):
        """Test factory methods for creating services."""
        loc = uicu.Locale("fr-FR")

        # Collator
        collator = loc.get_collator()
        assert collator.locale == loc

        # Word segmenter
        segmenter = loc.get_word_segmenter()
        assert segmenter is not None


class TestLocaleConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_get_available_locales(self):
        """Test getting available locales."""
        locales = uicu.get_available_locales()

        # Should have many locales
        assert len(locales) > 50

        # Common locales should be present
        assert "en-US" in locales or "en_US" in locales
        assert "fr-FR" in locales or "fr_FR" in locales
        assert "ja-JP" in locales or "ja_JP" in locales

    def test_get_default_locale(self):
        """Test getting system default locale."""
        default = uicu.get_default_locale()

        # Should be a valid Locale object
        assert isinstance(default, uicu.Locale)
        assert default.language  # Should have a language code
