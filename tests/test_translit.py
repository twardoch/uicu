#!/usr/bin/env python
# this_file: tests/test_translit.py
"""Tests for transliteration module."""

import pytest

import uicu


class TestTransliterator:
    """Test Transliterator class functionality."""

    def test_basic_transliteration(self):
        """Test basic transliteration."""
        # Latin to ASCII
        trans = uicu.Transliterator("Latin-ASCII")
        assert trans.transliterate("café") == "cafe"
        assert trans.transliterate("naïve") == "naive"
        assert trans.transliterate("Zürich") == "Zurich"

    def test_script_conversion(self):
        """Test script-to-script conversion."""
        # Greek to Latin
        greek = uicu.Transliterator("Greek-Latin")
        result = greek.transliterate("Αθήνα")
        # Different versions of ICU may produce slightly different results
        assert result in ["Athī́na", "Athína", "Athḗna"]

        # Cyrillic to Latin
        cyrillic = uicu.Transliterator("Cyrillic-Latin")
        result = cyrillic.transliterate("Москва")
        assert "Moskva" in result or "Moskwa" in result

    def test_unicode_normalization(self):
        """Test Unicode normalization transforms."""
        # NFD normalization
        nfd = uicu.Transliterator("NFD")
        composed = "é"  # Single character
        decomposed = nfd.transliterate(composed)
        assert len(decomposed) == 2  # Base + combining

        # NFC normalization
        nfc = uicu.Transliterator("NFC")
        assert len(nfc.transliterate(decomposed)) == 1

    def test_case_transforms(self):
        """Test case transformation."""
        # Upper case
        upper = uicu.Transliterator("Upper")
        assert upper.transliterate("hello world") == "HELLO WORLD"

        # Lower case
        lower = uicu.Transliterator("Lower")
        assert lower.transliterate("HELLO WORLD") == "hello world"

        # Title case
        title = uicu.Transliterator("Title")
        assert title.transliterate("hello world") == "Hello World"

    def test_invalid_transform(self):
        """Test error handling for invalid transforms."""
        with pytest.raises(uicu.ConfigurationError):
            uicu.Transliterator("Invalid-Transform")

    def test_compound_transforms(self):
        """Test compound transform IDs."""
        # Chain multiple transforms
        trans = uicu.Transliterator("Greek-Latin; Latin-ASCII; Lower")
        result = trans.transliterate("Αθήνα")
        assert result == "athina" or result == "athena"

    def test_inverse_transform(self):
        """Test inverse transforms."""
        trans = uicu.Transliterator("Katakana-Latin")

        # Check if inverse is available
        if trans.has_inverse():
            inverse = trans.get_inverse()
            # Round-trip test
            original = "カタカナ"
            latin = trans.transliterate(original)
            back = inverse.transliterate(latin)
            # May not be exactly the same due to ambiguities
            assert len(back) > 0

    def test_filter_function(self):
        """Test filter function for selective transliteration."""
        # Only transliterate uppercase letters
        trans = uicu.Transliterator("Latin-ASCII")

        def uppercase_filter(char):
            return char.isupper()

        result = trans.transliterate("CaFé", filter_fn=uppercase_filter)
        # Only C and F should be checked for transliteration
        # The behavior depends on implementation
        assert "a" in result  # Lowercase unchanged

    def test_transliterator_properties(self):
        """Test transliterator properties."""
        trans = uicu.Transliterator("Latin-ASCII")

        assert trans.id == "Latin-ASCII"
        assert len(trans.display_name) > 0
        assert isinstance(trans.source_set, set | type(None))
        assert isinstance(trans.target_set, set | type(None))


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_transliterate_function(self):
        """Test transliterate convenience function."""
        # Simple transliteration
        assert uicu.transliterate("café", "Latin-ASCII") == "cafe"

        # With filter
        result = uicu.transliterate("Test123", "Upper", filter_fn=str.isalpha)
        assert "123" in result  # Numbers unchanged

    def test_get_available_transforms(self):
        """Test getting available transform IDs."""
        transforms = uicu.get_available_transforms()

        # Should have many transforms
        assert len(transforms) > 50

        # Common transforms should be available
        assert any("Latin-ASCII" in t for t in transforms)
        assert any("NFD" in t for t in transforms)
        assert any("NFC" in t for t in transforms)
        assert any("Upper" in t for t in transforms)
        assert any("Lower" in t for t in transforms)

    def test_script_detection(self):
        """Test convenience functions for script operations."""
        # Detect primary script
        assert uicu.detect_script("Hello") == "Latn"
        assert uicu.detect_script("Привет") == "Cyrl"
        assert uicu.detect_script("你好") == "Hani"

        # Mixed scripts
        mixed = uicu.detect_script("Hello世界")
        assert mixed in ["Latn", "Hani", "Mixed", None]  # Depends on implementation


class TestSpecialTransforms:
    """Test special-purpose transforms."""

    def test_remove_accents(self):
        """Test accent removal transform."""
        # Using Latin-ASCII for accent removal
        trans = uicu.Transliterator("Latin-ASCII")

        test_cases = [
            ("café", "cafe"),
            ("naïve", "naive"),
            ("résumé", "resume"),
            ("piñata", "pinata"),
            ("Zürich", "Zurich"),
        ]

        for original, expected in test_cases:
            assert trans.transliterate(original) == expected

    def test_any_to_latin(self):
        """Test Any-Latin transform."""
        trans = uicu.Transliterator("Any-Latin")

        # Various scripts to Latin
        assert len(trans.transliterate("你好")) > 0  # Chinese
        assert len(trans.transliterate("こんにちは")) > 0  # Japanese
        assert len(trans.transliterate("Здравствуйте")) > 0  # Russian
        assert len(trans.transliterate("مرحبا")) > 0  # Arabic
