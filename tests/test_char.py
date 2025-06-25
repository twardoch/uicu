#!/usr/bin/env python
# this_file: tests/test_char.py
"""Tests for Unicode character properties module."""

import pytest

import uicu


class TestCharacterProperties:
    """Test basic character property functions."""

    def test_name(self):
        """Test character name lookup."""
        assert uicu.name("A") == "LATIN CAPITAL LETTER A"
        assert uicu.name("你") == "CJK UNIFIED IDEOGRAPH-4F60"
        assert uicu.name("🐍") == "SNAKE"

        # Test with codepoint
        assert uicu.name(65) == "LATIN CAPITAL LETTER A"

        # Test with default
        assert uicu.name("\x00", "NULL") == "NULL"

    def test_category(self):
        """Test general category."""
        assert uicu.category("A") == "Lu"  # Uppercase letter
        assert uicu.category("a") == "Ll"  # Lowercase letter
        assert uicu.category("1") == "Nd"  # Decimal number
        assert uicu.category(" ") == "Zs"  # Space separator
        assert uicu.category("!") == "Po"  # Other punctuation

    def test_bidirectional(self):
        """Test bidirectional class."""
        assert uicu.bidirectional("A") == "L"  # Left-to-right
        assert uicu.bidirectional("א") == "R"  # Right-to-left (Hebrew)
        assert uicu.bidirectional("١") == "AN"  # Arabic-Indic digit (intentional)  # noqa: RUF001

    def test_combining(self):
        """Test combining class."""
        assert uicu.combining("A") == 0  # Not combining
        assert uicu.combining("\u0301") > 0  # Combining acute accent

    def test_mirrored(self):
        """Test mirrored property."""
        assert not uicu.mirrored("A")
        assert uicu.mirrored("(")  # Parentheses are mirrored
        assert uicu.mirrored("[")  # Brackets are mirrored

    def test_numeric_values(self):
        """Test numeric value functions."""
        # Decimal
        assert uicu.decimal("5") == 5
        assert uicu.decimal("A") is None  # No decimal value
        assert uicu.decimal("A", -1) == -1

        # Digit
        assert uicu.digit("7") == 7
        assert uicu.digit("A") is None  # No digit value

        # Numeric (includes fractions)
        assert uicu.numeric("9") == 9
        assert uicu.numeric("½") == 0.5
        assert uicu.numeric("¾") == 0.75


class TestScriptAndBlock:
    """Test script and block properties (requires fontTools)."""

    @pytest.mark.skipif(not hasattr(uicu, "script"), reason="fontTools not available")
    def test_script(self):
        """Test script identification."""
        assert uicu.script("A") == "Latn"
        assert uicu.script("你") == "Hani"
        assert uicu.script("א") == "Hebr"
        assert uicu.script("ก") == "Thai"
        assert uicu.script("😀") == "Zyyy"  # Common script for emoji

    @pytest.mark.skipif(not hasattr(uicu, "script_name"), reason="fontTools not available")
    def test_script_name(self):
        """Test script name lookup."""
        assert uicu.script_name("Latn") == "Latin"
        assert uicu.script_name("Hani") == "Han"
        assert uicu.script_name("Arab") == "Arabic"

    @pytest.mark.skipif(not hasattr(uicu, "block"), reason="fontTools not available")
    def test_block(self):
        """Test block identification."""
        assert uicu.block("A") == "Basic Latin"
        assert "CJK" in uicu.block("你")
        assert "Hebrew" in uicu.block("א")


class TestCharClass:
    """Test the Char class."""

    def test_char_creation(self):
        """Test creating Char objects."""
        # From string
        ch = uicu.Char("A")
        assert ch.char == "A"
        assert ch.codepoint == 65

        # From codepoint
        ch2 = uicu.Char(65)
        assert ch2.char == "A"
        assert ch2 == ch

    def test_char_properties(self):
        """Test Char object properties."""
        ch = uicu.Char("€")
        assert ch.name == "EURO SIGN"
        assert ch.category == "Sc"  # Currency symbol
        assert ch.decimal is None
        assert not ch.mirrored

    def test_char_string_methods(self):
        """Test string representation."""
        ch = uicu.Char("A")
        assert str(ch) == "A"
        assert "A" in repr(ch)
        assert "U+0041" in repr(ch)

    def test_char_comparison(self):
        """Test character comparison."""
        ch1 = uicu.Char("A")
        ch2 = uicu.Char("A")
        ch3 = uicu.Char("B")

        assert ch1 == ch2
        assert ch1 != ch3
        assert ch1 == "A"
        assert ch1 != "B"
