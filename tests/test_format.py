#!/usr/bin/env python
# this_file: tests/test_format.py
"""Tests for formatting module."""

from datetime import datetime, timezone

import pytest

import uicu
from uicu.exceptions import OperationError


class TestDateTimeFormatter:
    """Test DateTimeFormatter functionality."""

    def test_basic_formatting(self):
        """Test basic date/time formatting."""
        formatter = uicu.DateTimeFormatter("en-US")
        dt = datetime(2025, 1, 25, 15, 30, 45, tzinfo=timezone.utc)

        result = formatter.format(dt)
        assert "2025" in result
        assert "Jan" in result or "January" in result
        assert "25" in result
        assert "3" in result or "15" in result
        assert "30" in result
        assert "45" in result

    def test_style_options(self):
        """Test different date/time styles."""
        dt = datetime(2025, 1, 25, 15, 30, 45, tzinfo=timezone.utc)

        # Full style
        formatter = uicu.DateTimeFormatter("en-US", date_style="full", time_style="full")
        result = formatter.format(dt)
        assert "Saturday" in result
        assert "January" in result
        assert "2025" in result
        assert "Pacific" in result or "Eastern" in result or "UTC" in result or "Greenwich Mean Time" in result

        # Short style
        formatter = uicu.DateTimeFormatter("en-US", date_style="short", time_style="short")
        result = formatter.format(dt)
        assert "1/25/25" in result or "1/25/2025" in result
        assert "3:30" in result or "15:30" in result

    def test_locale_formatting(self):
        """Test formatting with different locales."""
        dt = datetime(2025, 1, 25, 15, 30, 45, tzinfo=timezone.utc)

        # French
        formatter = uicu.DateTimeFormatter("fr-FR")
        result = formatter.format(dt)
        assert "janv." in result or "janvier" in result
        assert "2025" in result

        # German (default medium style uses numeric format)
        formatter = uicu.DateTimeFormatter("de-DE")
        result = formatter.format(dt)
        assert "25.01.2025" in result or "Jan" in result or "Januar" in result
        assert "2025" in result

    def test_custom_pattern(self):
        """Test custom pattern formatting."""
        dt = datetime(2025, 1, 25, 15, 30, 45, tzinfo=timezone.utc)

        # Custom pattern
        formatter = uicu.DateTimeFormatter("en-US", pattern="yyyy-MM-dd HH:mm:ss")
        result = formatter.format(dt)
        assert result == "2025-01-25 15:30:45"

        # Another pattern
        formatter = uicu.DateTimeFormatter("en-US", pattern="MMMM d, yyyy")
        result = formatter.format(dt)
        assert result == "January 25, 2025"

    def test_skeleton_pattern(self):
        """Test skeleton pattern formatting."""
        dt = datetime(2025, 1, 25, 15, 30, 45, tzinfo=timezone.utc)

        # Skeleton pattern
        formatter = uicu.DateTimeFormatter("en-US", skeleton="yMMMdhm")
        result = formatter.format(dt)
        assert "Jan" in result
        assert "25" in result
        assert "2025" in result
        assert "3:30" in result or "15:30" in result

    def test_format_range(self):
        """Test date range formatting."""
        formatter = uicu.DateTimeFormatter("en-US", date_style="medium", time_style="none")

        start = datetime(2025, 1, 3, tzinfo=timezone.utc)
        end = datetime(2025, 1, 5, tzinfo=timezone.utc)

        result = formatter.format_range(start, end)

        # Check key parts are present
        assert "Jan" in result
        assert "3" in result
        assert "5" in result
        # Should use hyphen
        assert "-" in result

    def test_locale_factory(self):
        """Test creating formatter from locale."""
        locale = uicu.Locale("fr-FR")
        formatter = locale.get_datetime_formatter(date_style="long", time_style="short")

        dt = datetime(2025, 1, 25, 15, 30, tzinfo=timezone.utc)
        result = formatter.format(dt)
        assert "janvier" in result
        assert "2025" in result
        assert "15:30" in result or "3:30" in result

    def test_invalid_configuration(self):
        """Test error handling for invalid configuration."""
        # Invalid style
        with pytest.raises(OperationError):
            uicu.DateTimeFormatter("en-US", date_style="invalid")

        with pytest.raises(OperationError):
            uicu.DateTimeFormatter("en-US", time_style="invalid")

    def test_parsing_errors(self):
        """Test parsing error handling."""
        pytest.skip("Parse method has been removed for v1.0 MVP")

    def test_repr(self):
        """Test string representation."""
        formatter = uicu.DateTimeFormatter("en-US", date_style="long", time_style="short")
        repr_str = repr(formatter)
        assert "DateTimeFormatter" in repr_str
        assert "en-US" in repr_str
        assert "long" in repr_str
        assert "short" in repr_str

        # With pattern
        formatter = uicu.DateTimeFormatter("en-US", pattern="yyyy-MM-dd")
        repr_str = repr(formatter)
        assert "pattern" in repr_str
        assert "yyyy-MM-dd" in repr_str
