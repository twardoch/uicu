#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING

import icu

from uicu._utils import ensure_locale
from uicu.exceptions import OperationError

if TYPE_CHECKING:
    from datetime import datetime, tzinfo

    from uicu.locale import Locale

# this_file: src/uicu/format.py
"""Locale-aware formatting for dates, numbers, lists, and messages.

This module provides Pythonic interfaces for ICU's formatting functionality,
enabling locale-sensitive formatting of dates, times, numbers, currencies,
lists, and complex messages.
"""


class DateTimeFormatter:
    """Formats datetime objects according to locale conventions.

    This class provides locale-aware formatting for dates and times,
    supporting various styles, custom patterns, and timezone handling.
    """

    def __init__(
        self,
        locale: str | Locale,
        date_style: str = "medium",
        time_style: str = "medium",
        pattern: str | None = None,
        skeleton: str | None = None,
        tz: str | tzinfo | None = None,
    ):
        """Initialize a date/time formatter.

        Styles: 'full', 'long', 'medium', 'short', 'none'.
        Pattern overrides styles (e.g., 'yyyy-MM-dd').
        Skeleton is flexible pattern (e.g., 'yMMMd').

        Examples:
            >>> formatter = DateTimeFormatter('en-US')
            >>> formatter.format(datetime.now())
            'Jan 25, 2025, 3:45:30 PM'

            >>> formatter = DateTimeFormatter('en-US', pattern='EEEE, MMMM d, yyyy')
            >>> formatter.format(datetime(2025, 1, 25))
            'Saturday, January 25, 2025'
        """
        # Convert string locale to Locale object if needed
        locale = ensure_locale(locale)

        self._locale = locale
        self._date_style = date_style
        self._time_style = time_style
        self._pattern = pattern
        self._skeleton = skeleton

        # Create formatter based on provided options
        if pattern:
            # Use custom pattern
            self._formatter = icu.SimpleDateFormat(pattern, locale._icu_locale)
        elif skeleton:
            # Use skeleton pattern with pattern generator
            pg = icu.DateTimePatternGenerator.createInstance(locale._icu_locale)
            best_pattern = pg.getBestPattern(skeleton)
            self._formatter = icu.SimpleDateFormat(best_pattern, locale._icu_locale)
        else:
            # Use style-based formatter
            style_map = {
                "full": icu.DateFormat.kFull,
                "long": icu.DateFormat.kLong,
                "medium": icu.DateFormat.kMedium,
                "short": icu.DateFormat.kShort,
                "none": -1,
            }

            date_style_val = style_map.get(date_style)
            time_style_val = style_map.get(time_style)

            if date_style_val is None:
                msg = f"Invalid date_style '{date_style}'. Must be one of: full, long, medium, short, none"
                raise OperationError(msg)
            if time_style_val is None:
                msg = f"Invalid time_style '{time_style}'. Must be one of: full, long, medium, short, none"
                raise OperationError(msg)

            self._formatter = icu.DateFormat.createDateTimeInstance(date_style_val, time_style_val, locale._icu_locale)

        # Set timezone if provided
        if tz:
            self._set_timezone(tz)

    def _set_timezone(self, tz: str | tzinfo):
        """Set the timezone for formatting.

        Args:
            tz: Timezone identifier string or Python tzinfo object.
        """
        if isinstance(tz, str):
            # String timezone ID
            icu_tz = icu.TimeZone.createTimeZone(tz)
        elif hasattr(tz, "tzname"):
            # Python tzinfo object - try to get timezone ID
            tz_name = tz.tzname(None)
            if tz_name:
                icu_tz = icu.TimeZone.createTimeZone(tz_name)
            else:
                # Fall back to UTC offset
                offset = tz.utcoffset(None)
                if offset:
                    hours = int(offset.total_seconds() // 3600)
                    minutes = int((offset.total_seconds() % 3600) // 60)
                    icu_tz = icu.SimpleTimeZone(hours * 60 + minutes, "Custom")
                else:
                    icu_tz = icu.TimeZone.getGMT()
        else:
            msg = f"Invalid timezone type: {type(tz)}"
            raise OperationError(msg)

        self._formatter.setTimeZone(icu_tz)

    def format(self, dt: datetime) -> str:
        """Format a datetime object to a string.

        Args:
            dt: The datetime to format.

        Returns:
            The formatted date/time string.

        Raises:
            OperationError: If formatting fails.

        Examples:
            >>> formatter = DateTimeFormatter('fr-FR', date_style='long',
            ...                              time_style='short')
            >>> formatter.format(datetime(2025, 1, 25, 15, 30))
            '25 janvier 2025 à 15:30'
        """
        # Create ICU Calendar and set the datetime
        cal = icu.GregorianCalendar()
        # Note: ICU months are 0-based
        cal.set(dt.year, dt.month - 1, dt.day, dt.hour, dt.minute, dt.second)
        cal.set(icu.Calendar.MILLISECOND, dt.microsecond // 1000)

        # If datetime has timezone info, set it
        if dt.tzinfo:
            tz_name = dt.tzinfo.tzname(dt)
            if tz_name == "UTC":
                # Handle UTC explicitly
                tz = icu.TimeZone.getGMT()
                cal.setTimeZone(tz)
                self._formatter.setTimeZone(tz)
            elif tz_name:
                tz = icu.TimeZone.createTimeZone(tz_name)
                cal.setTimeZone(tz)
                self._formatter.setTimeZone(tz)

        # Get the ICU time value
        icu_time = cal.getTime()

        return self._formatter.format(icu_time)

    def format_range(self, start: datetime, end: datetime) -> str:
        """Format a date/time range.

        Args:
            start: Start date/time
            end: End date/time

        Returns:
            str: Formatted range

        Example:
            >>> formatter = DateTimeFormatter('en-US', date_style='medium', time_style='none')
            >>> start = datetime(2025, 1, 3)
            >>> end = datetime(2025, 1, 5)
            >>> formatter.format_range(start, end)
            'Jan 3 - 5, 2025'
        """
        # Simple range formatting using individual format calls
        # TODO: Implement proper ICU DateIntervalFormat when available
        start_str = self.format(start)
        end_str = self.format(end)

        # Simple range formatting - just join with dash
        # In a full implementation, this would use proper interval formatting
        if start.date() == end.date():
            # Same date, just show date once
            result = start_str
        # Different dates - create simple range
        # Extract just the date parts for cleaner range display
        elif "," in start_str and "," in end_str:
            start_date = start_str.split(",")[0].strip()
            end_date = end_str.split(",")[0].strip()
            if start_date.split()[-1] == end_date.split()[-1]:  # Same year
                # Same year, can shorten format
                start_short = " ".join(start_date.split()[:-1])
                result = f"{start_short} - {end_date}"
            else:
                result = f"{start_date} - {end_date}"
        else:
            result = f"{start_str} - {end_str}"

        return result.replace("-", "-")  # Use standard hyphen instead of en dash

    @property
    def pattern(self) -> str | None:
        """Get the pattern used by this formatter."""
        if self._pattern:
            return self._pattern
        if isinstance(self._formatter, icu.SimpleDateFormat):
            return self._formatter.toPattern()
        return None

    @property
    def locale(self) -> Locale:
        """Get the locale used by this formatter."""
        return self._locale

    def __repr__(self) -> str:
        """Return string representation."""
        parts = [f"locale='{self._locale.language_tag}'"]
        if self._pattern:
            parts.append(f"pattern='{self._pattern}'")
        elif self._skeleton:
            parts.append(f"skeleton='{self._skeleton}'")
        else:
            parts.append(f"date_style='{self._date_style}'")
            parts.append(f"time_style='{self._time_style}'")
        return f"DateTimeFormatter({', '.join(parts)})"
