#!/usr/bin/env python
# this_file: src/uicu/format.py
"""Locale-aware formatting for dates, numbers, lists, and messages.

This module provides Pythonic interfaces for ICU's formatting functionality,
enabling locale-sensitive formatting of dates, times, numbers, currencies,
lists, and complex messages.
"""

from datetime import datetime, tzinfo

import icu

from uicu._utils import ensure_locale
from uicu.exceptions import OperationError
from uicu.locale import Locale

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
            if tz_name:
                tz = icu.TimeZone.createTimeZone(tz_name)
                cal.setTimeZone(tz)

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
        # Create interval formatter with same style
        # For date intervals, we typically don't want time
        skeleton = "yMMMd" if self._time_style == "none" or self._date_style == "none" else "yMMMdjm"

        dtifmt = icu.DateIntervalFormat.createInstance(skeleton, self._locale._icu_locale)

        # Convert Python datetimes to ICU timestamps
        start_ts = int(start.timestamp() * 1000)  # ICU uses milliseconds
        end_ts = int(end.timestamp() * 1000)

        # Format the range
        from_field = icu.FieldPosition(0)
        to_field = icu.FieldPosition(0)
        result = dtifmt.format((start_ts, end_ts), from_field, to_field)

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


class NumberFormatter:
    """Formats numbers according to locale conventions.

    This class provides locale-aware formatting for numbers, currencies,
    percentages, and scientific notation.
    """

    def __init__(
        self,
        locale: str | Locale,
        style: str = "decimal",
        min_fraction_digits: int | None = None,
        max_fraction_digits: int | None = None,
        min_integer_digits: int | None = None,
        *,
        grouping: bool = True,
        rounding_mode: str = "half_even",
    ):
        """Initialize a number formatter.

        Styles: 'decimal', 'currency', 'percent', 'scientific'.
        Rounding modes: 'ceiling', 'floor', 'half_even', 'half_up'.

        Examples:
            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format(1234.56)
            '1,234.56'

            >>> formatter = NumberFormatter('de-DE', style='currency')
            >>> formatter.format_currency(1234.56, 'EUR')
            '1.234,56 €'
        """
        # Convert string locale to Locale object if needed
        locale = ensure_locale(locale)

        self._locale = locale
        self._style = style
        self._min_fraction_digits = min_fraction_digits
        self._max_fraction_digits = max_fraction_digits
        self._min_integer_digits = min_integer_digits
        self._grouping = grouping
        self._rounding_mode = rounding_mode

        # Create ICU number formatter based on style
        if style == "decimal":
            self._formatter = icu.NumberFormat.createInstance(locale._icu_locale)
        elif style == "currency":
            self._formatter = icu.NumberFormat.createCurrencyInstance(locale._icu_locale)
        elif style == "percent":
            self._formatter = icu.NumberFormat.createPercentInstance(locale._icu_locale)
        elif style == "scientific":
            self._formatter = icu.NumberFormat.createScientificInstance(locale._icu_locale)
        else:
            msg = f"Invalid style '{style}'. Must be one of: decimal, currency, percent, scientific"
            raise OperationError(msg)

        # Configure formatter options
        if min_fraction_digits is not None:
            self._formatter.setMinimumFractionDigits(min_fraction_digits)
        if max_fraction_digits is not None:
            self._formatter.setMaximumFractionDigits(max_fraction_digits)
        if min_integer_digits is not None:
            self._formatter.setMinimumIntegerDigits(min_integer_digits)

        self._formatter.setGroupingUsed(grouping)

        # Set rounding mode
        rounding_map = {
            "ceiling": icu.DecimalFormat.kRoundCeiling,
            "floor": icu.DecimalFormat.kRoundFloor,
            "half_even": icu.DecimalFormat.kRoundHalfEven,
            "half_up": icu.DecimalFormat.kRoundHalfUp,
        }
        if rounding_mode in rounding_map:
            if hasattr(self._formatter, "setRoundingMode"):
                self._formatter.setRoundingMode(rounding_map[rounding_mode])

    def format(self, number: float) -> str:
        """Format a number according to the configured style.

        Examples:
            >>> formatter = NumberFormatter('fr-FR')
            >>> formatter.format(1234.56)
            '1 234,56'

            >>> formatter = NumberFormatter('en-US', style='percent')
            >>> formatter.format(0.1234)
            '12.34%'
        """
        return self._formatter.format(number)

    def format_currency(self, amount: float, currency: str) -> str:
        """Format a number as currency.

        Args:
            amount: The numeric amount to format.
            currency: ISO 4217 currency code (e.g., 'USD', 'EUR').

        Examples:
            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format_currency(1234.56, 'USD')
            '$1,234.56'

            >>> formatter = NumberFormatter('ja-JP')
            >>> formatter.format_currency(1234, 'JPY')
            '￥1,234'
        """
        # Create a currency instance for the specific currency
        currency_formatter = icu.NumberFormat.createCurrencyInstance(self._locale._icu_locale)

        # Apply the same settings as our main formatter
        if self._min_fraction_digits is not None:
            currency_formatter.setMinimumFractionDigits(self._min_fraction_digits)
        if self._max_fraction_digits is not None:
            currency_formatter.setMaximumFractionDigits(self._max_fraction_digits)
        if self._min_integer_digits is not None:
            currency_formatter.setMinimumIntegerDigits(self._min_integer_digits)

        currency_formatter.setGroupingUsed(self._grouping)

        # Set the currency
        currency_unit = icu.CurrencyUnit(currency)
        currency_formatter.setCurrency(currency_unit)

        return currency_formatter.format(amount)

    def format_compact(self, number: float, notation: str = "short") -> str:
        """Format a number using compact notation (1.2K, 3.4M).

        Args:
            number: The number to format.
            notation: 'short' (1.2K) or 'long' (1.2 thousand).

        Examples:
            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format_compact(1234)
            '1.2K'

            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format_compact(1234, 'long')
            '1.2 thousand'

            >>> formatter = NumberFormatter('de-DE')
            >>> formatter.format_compact(1234567)
            '1,2 Mio.'
        """
        try:
            # Create compact number formatter
            if notation == "short":
                compact_formatter = icu.NumberFormat.createCompactDecimalInstance(
                    self._locale._icu_locale, icu.NumberFormat.kCompactShort
                )
            elif notation == "long":
                compact_formatter = icu.NumberFormat.createCompactDecimalInstance(
                    self._locale._icu_locale, icu.NumberFormat.kCompactLong
                )
            else:
                msg = f"Invalid notation '{notation}'. Must be 'short' or 'long'"
                raise OperationError(msg)

            # Apply the same settings as our main formatter
            if self._min_fraction_digits is not None:
                compact_formatter.setMinimumFractionDigits(self._min_fraction_digits)
            if self._max_fraction_digits is not None:
                compact_formatter.setMaximumFractionDigits(self._max_fraction_digits)

            compact_formatter.setGroupingUsed(self._grouping)

            return compact_formatter.format(number)
        except Exception:
            # Fallback to regular formatting if compact not available
            return self.format(number)

    def format_range(self, start: float, end: float) -> str:
        """Format a number range.

        Args:
            start: Start of the range.
            end: End of the range.

        Examples:
            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format_range(10, 20)
            '10-20'

            >>> formatter = NumberFormatter('de-DE', style='currency')
            >>> formatter.format_range(10.50, 25.75, 'EUR')
            '10,50 €-25,75 €'
        """
        try:
            # Create range formatter
            range_formatter = icu.NumberRangeFormatter.withLocale(self._locale._icu_locale)

            # Configure based on our style
            if self._style == "currency":
                # For currency ranges, we need to specify currency in the call
                # This is a simplified implementation
                start_formatted = self.format(start)
                end_formatted = self.format(end)
                return f"{start_formatted}-{end_formatted}"
            if self._style == "percent":
                range_formatter = range_formatter.numberFormatterBoth(
                    icu.NumberFormatter.withLocale(self._locale._icu_locale).unit(
                        icu.MeasureUnit.forIdentifier("percent")
                    )
                )

            return range_formatter.formatFormattableRange(start, end).toString()
        except Exception:
            # Fallback to simple range formatting
            start_formatted = self.format(start)
            end_formatted = self.format(end)
            return f"{start_formatted}-{end_formatted}"

    @property
    def locale(self) -> Locale:
        """Get the locale used by this formatter."""
        return self._locale

    @property
    def style(self) -> str:
        """Get the style used by this formatter."""
        return self._style

    def __repr__(self) -> str:
        """Return string representation."""
        parts = [f"locale='{self._locale.language_tag}'", f"style='{self._style}'"]
        if self._min_fraction_digits is not None:
            parts.append(f"min_fraction_digits={self._min_fraction_digits}")
        if self._max_fraction_digits is not None:
            parts.append(f"max_fraction_digits={self._max_fraction_digits}")
        return f"NumberFormatter({', '.join(parts)})"


class ListFormatter:
    """Formats lists according to locale conventions.

    This class provides locale-aware formatting for lists, supporting
    different list types (and, or, units) and styles.
    """

    def __init__(
        self,
        locale: str | Locale,
        list_type: str = "and",
        style: str = "standard",
    ):
        """Initialize a list formatter.

        List types: 'and', 'or', 'units'.
        Styles: 'standard', 'short', 'narrow'.

        Examples:
            >>> formatter = ListFormatter('en-US')
            >>> formatter.format(['apples', 'oranges', 'bananas'])
            'apples, oranges, and bananas'

            >>> formatter = ListFormatter('en-US', list_type='or')
            >>> formatter.format(['red', 'blue'])
            'red or blue'

            >>> formatter = ListFormatter('es-ES', list_type='and')
            >>> formatter.format(['manzanas', 'naranjas'])
            'manzanas y naranjas'
        """
        # Convert string locale to Locale object if needed
        locale = ensure_locale(locale)

        self._locale = locale
        self._list_type = list_type
        self._style = style

        # Validate list type
        valid_types = {"and", "or", "units"}
        if list_type not in valid_types:
            msg = f"Invalid list_type '{list_type}'. Must be one of: {', '.join(valid_types)}"
            raise OperationError(msg)

        # Validate style
        valid_styles = {"standard", "short", "narrow"}
        if style not in valid_styles:
            msg = f"Invalid style '{style}'. Must be one of: {', '.join(valid_styles)}"
            raise OperationError(msg)

        # Create ICU list formatter
        # Map our types to ICU types
        type_map = {
            "and": icu.ListFormatter.kAnd,
            "or": icu.ListFormatter.kOr,
            "units": icu.ListFormatter.kUnits,
        }

        # Map our styles to ICU styles
        style_map = {
            "standard": icu.ListFormatter.kStandard,
            "short": icu.ListFormatter.kShort,
            "narrow": icu.ListFormatter.kNarrow,
        }

        self._formatter = icu.ListFormatter.createInstance(locale._icu_locale, type_map[list_type], style_map[style])

    def format(self, items: list[str]) -> str:
        """Format a list of strings according to locale conventions.

        Args:
            items: List of strings to format.

        Returns:
            Formatted list string.

        Raises:
            OperationError: If formatting fails.

        Examples:
            >>> formatter = ListFormatter('en-US')
            >>> formatter.format(['apple'])
            'apple'

            >>> formatter = ListFormatter('en-US')
            >>> formatter.format(['apple', 'orange'])
            'apple and orange'

            >>> formatter = ListFormatter('fr-FR', list_type='or')
            >>> formatter.format(['rouge', 'bleu', 'vert'])
            'rouge, bleu ou vert'
        """
        if not items:
            return ""

        if len(items) == 1:
            return items[0]

        # Convert to ICU string list
        string_list = [str(item) for item in items]
        return self._formatter.format(string_list)

    @property
    def locale(self) -> Locale:
        """Get the locale used by this formatter."""
        return self._locale

    @property
    def list_type(self) -> str:
        """Get the list type used by this formatter."""
        return self._list_type

    @property
    def style(self) -> str:
        """Get the style used by this formatter."""
        return self._style

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"ListFormatter(locale='{self._locale.language_tag}', list_type='{self._list_type}', style='{self._style}')"
        )
