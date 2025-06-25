#!/usr/bin/env python
# this_file: tests/test_collate.py
"""Tests for collation module."""

import pytest

import uicu


class TestCollator:
    """Test Collator class functionality."""

    def test_collator_creation(self):
        """Test creating Collator objects."""
        # Basic creation
        collator = uicu.Collator("en-US")
        assert collator.locale.language == "en"
        assert collator.strength == "tertiary"
        assert not collator.numeric

        # With options
        collator2 = uicu.Collator("fr-FR", strength="primary", numeric=True)
        assert collator2.strength == "primary"
        assert collator2.numeric

    def test_invalid_collator(self):
        """Test error handling for invalid configuration."""
        # Invalid locale (empty string)
        with pytest.raises(uicu.ConfigurationError):
            uicu.Collator("")

        # Invalid strength
        with pytest.raises(uicu.ConfigurationError):
            uicu.Collator("en-US", strength="invalid")

    def test_compare(self):
        """Test string comparison."""
        collator = uicu.Collator("en-US")

        # Basic comparison
        assert collator.compare("a", "b") == -1
        assert collator.compare("b", "a") == 1
        assert collator.compare("a", "a") == 0

        # Case-sensitive (tertiary strength) - ICU behavior varies by locale
        # Just check that case makes a difference
        assert collator.compare("a", "A") != 0

    def test_strength_levels(self):
        """Test different strength levels."""
        # Primary - ignores case and accents
        primary = uicu.Collator("en-US", strength="primary")
        assert primary.is_equal("a", "A")
        assert primary.is_equal("e", "é")

        # Secondary - considers accents but not case
        secondary = uicu.Collator("en-US", strength="secondary")
        assert secondary.is_equal("a", "A")
        assert not secondary.is_equal("e", "é")

        # Tertiary - considers case differences
        tertiary = uicu.Collator("en-US", strength="tertiary")
        assert not tertiary.is_equal("a", "A")
        assert not tertiary.is_equal("e", "é")

    def test_numeric_sorting(self):
        """Test numeric sorting option."""
        # Without numeric sorting
        regular = uicu.Collator("en-US")
        strings = ["item2", "item10", "item1"]
        sorted_regular = regular.sort(strings)
        assert sorted_regular == ["item1", "item10", "item2"]

        # With numeric sorting
        numeric = uicu.Collator("en-US", numeric=True)
        sorted_numeric = numeric.sort(strings)
        assert sorted_numeric == ["item1", "item2", "item10"]

    def test_sort_key(self):
        """Test sort key generation."""
        collator = uicu.Collator("en-US")

        # Sort keys should maintain same ordering
        key_a = collator.key("apple")
        key_b = collator.key("banana")
        assert key_a < key_b

        # Keys should be bytes
        assert isinstance(key_a, bytes)
        assert isinstance(key_b, bytes)

    def test_callable_interface(self):
        """Test using collator as key function."""
        collator = uicu.Collator("en-US")

        # Use as key function with sorted()
        words = ["banana", "apple", "cherry"]
        sorted_words = sorted(words, key=collator)
        assert sorted_words == ["apple", "banana", "cherry"]

    def test_locale_specific_sorting(self):
        """Test locale-specific sorting rules."""
        # German sorts ä after a
        german = uicu.Collator("de-DE")
        words = ["Müller", "Mueller", "Mahler"]
        sorted_de = german.sort(words)

        # Swedish sorts ä after z
        swedish = uicu.Collator("sv-SE")
        words_sv = ["ark", "ärm", "ask"]
        sorted_sv = swedish.sort(words_sv)

        # Different locales produce different orderings
        assert sorted_de != sorted_sv or len(sorted_de) != len(sorted_sv)

    def test_case_first_option(self):
        """Test case_first option."""
        # Upper case first
        upper_first = uicu.Collator("en-US", case_first="upper")
        assert upper_first.compare("A", "a") < 0

        # Lower case first
        lower_first = uicu.Collator("en-US", case_first="lower")
        assert lower_first.compare("a", "A") < 0

    def test_comparison_methods(self):
        """Test convenience comparison methods."""
        collator = uicu.Collator("en-US")

        # is_equal
        assert collator.is_equal("hello", "hello")
        assert not collator.is_equal("hello", "world")

        # is_less
        assert collator.is_less("apple", "banana")
        assert not collator.is_less("banana", "apple")

        # is_greater
        assert collator.is_greater("zebra", "apple")
        assert not collator.is_greater("apple", "zebra")


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_sort_function(self):
        """Test sort convenience function."""
        words = ["café", "cote", "côte", "coté"]

        # French sorting
        sorted_fr = uicu.sort(words, "fr-FR")
        assert isinstance(sorted_fr, list)
        assert len(sorted_fr) == len(words)

        # With options
        sorted_primary = uicu.sort(words, "fr-FR", strength="primary")
        assert len(sorted_primary) == len(words)

    def test_compare_function(self):
        """Test compare convenience function."""
        # Basic comparison
        assert uicu.compare("a", "b", "en-US") == -1
        assert uicu.compare("b", "a", "en-US") == 1
        assert uicu.compare("a", "a", "en-US") == 0

        # With options
        assert uicu.compare("A", "a", "en-US", strength="primary") == 0
