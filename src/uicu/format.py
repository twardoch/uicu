#!/usr/bin/env python
# this_file: src/uicu/format.py
"""Locale-aware formatting for dates, numbers, lists, and messages.

This module provides Pythonic interfaces for ICU's formatting functionality,
enabling locale-sensitive formatting of dates, times, numbers, currencies,
lists, and complex messages.
"""

from datetime import datetime, tzinfo
from typing import Any

import icu

from uicu.exceptions import ConfigurationError, OperationError
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
        timezone: str | tzinfo | None = None,
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
        if isinstance(locale, str):
            try:
                locale = Locale(locale)
            except Exception as e:
                msg = f"Invalid locale '{locale}': {e}"
                raise OperationError(msg) from e

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

            self._formatter = icu.DateFormat.createDateTimeInstance(
                date_style_val, time_style_val, locale._icu_locale
            )

        # Set timezone if provided
        if timezone:
            self._set_timezone(timezone)

    def _set_timezone(self, timezone: str | tzinfo):
        """Set the timezone for formatting.

        Args:
            timezone: Timezone identifier string or Python tzinfo object.
        """
        try:
            if isinstance(timezone, str):
                # String timezone ID
                tz = icu.TimeZone.createTimeZone(timezone)
            elif hasattr(timezone, "tzname"):
                # Python tzinfo object - try to get timezone ID
                tz_name = timezone.tzname(None)
                if tz_name:
                    tz = icu.TimeZone.createTimeZone(tz_name)
                else:
                    # Fall back to UTC offset
                    offset = timezone.utcoffset(None)
                    if offset:
                        hours = int(offset.total_seconds() // 3600)
                        minutes = int((offset.total_seconds() % 3600) // 60)
                        tz = icu.SimpleTimeZone(hours * 60 + minutes, "Custom")
                    else:
                        tz = icu.TimeZone.getGMT()
            else:
                msg = f"Invalid timezone type: {type(timezone)}"
                raise OperationError(msg)

            self._formatter.setTimeZone(tz)
        except Exception as e:
            msg = f"Failed to set timezone: {e}"
            raise OperationError(msg) from e

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

    def parse(self, text: str, lenient: bool = True) -> datetime:
        """Parse a string to a datetime object.

        Args:
            text: String to parse.
            lenient: If True, uses lenient parsing (more forgiving).
                    If False, uses strict parsing.

        Returns:
            Parsed datetime object.

        Raises:
            OperationError: If parsing fails.

        Examples:
            >>> formatter = DateTimeFormatter('en-US', date_style='medium')
            >>> dt = formatter.parse('Jan 25, 2025')
            >>> dt.year, dt.month, dt.day
            (2025, 1, 25)

            >>> formatter = DateTimeFormatter('en-US', pattern='yyyy-MM-dd')
            >>> dt = formatter.parse('2025-01-25')
            >>> dt.year, dt.month, dt.day
            (2025, 1, 25)
        """
        if not text.strip():
            raise OperationError("Cannot parse empty string")

        try:
            # Set lenient mode on the formatter
            if hasattr(self._formatter, 'setLenient'):
                self._formatter.setLenient(lenient)
            
            # For SimpleDateFormat, we can parse directly
            if isinstance(self._formatter, icu.SimpleDateFormat):
                # Parse using SimpleDateFormat
                parse_position = icu.ParsePosition(0)
                icu_date = self._formatter.parse(text, parse_position)
                
                # Check if parsing succeeded
                if parse_position.getErrorIndex() >= 0:
                    error_index = parse_position.getErrorIndex()
                    raise OperationError(f"Parse error at position {error_index} in '{text}'")
                
                if icu_date is None or parse_position.getIndex() == 0:
                    # Try alternative parsing methods
                    try:
                        # Try parsing without position tracking
                        icu_date = self._formatter.parse(text)
                        if icu_date is None:
                            raise OperationError(f"Unable to parse '{text}' with pattern '{self._formatter.toPattern()}'")
                    except Exception:
                        raise OperationError(f"Unable to parse '{text}' with pattern '{self._formatter.toPattern()}'")
                
                # Convert ICU date (seconds since epoch) to Python datetime
                dt = datetime.fromtimestamp(icu_date)
                return dt
            
            else:
                # For other date formatters, try to get a SimpleDateFormat
                pattern = self.pattern
                if pattern:
                    simple_formatter = icu.SimpleDateFormat(pattern, self._locale._icu_locale)
                    if hasattr(simple_formatter, 'setLenient'):
                        simple_formatter.setLenient(lenient)
                    
                    try:
                        icu_date = simple_formatter.parse(text)
                        if icu_date is None:
                            raise OperationError(f"Unable to parse '{text}' with pattern '{pattern}'")
                        
                        dt = datetime.fromtimestamp(icu_date)
                        return dt
                    except Exception as e:
                        raise OperationError(f"Failed to parse '{text}' with pattern '{pattern}': {e}")
                else:
                    # No pattern available, cannot parse
                    raise OperationError(f"Cannot parse with style-based formatter - use pattern-based formatter for parsing")
            
        except Exception as e:
            if isinstance(e, OperationError):
                raise
            msg = f"Failed to parse '{text}': {e}"
            raise OperationError(msg) from e

    def parse_strict(self, text: str) -> datetime:
        """Parse a string using strict parsing rules.

        This is a convenience method equivalent to parse(text, lenient=False).

        Args:
            text: String to parse.

        Returns:
            Parsed datetime object.

        Raises:
            OperationError: If parsing fails.
        """
        return self.parse(text, lenient=False)

    def format_range(self, start: datetime, end: datetime) -> str:
        """Format a datetime range.

        Args:
            start: Start datetime.
            end: End datetime.

        Returns:
            Formatted date/time range string.

        Raises:
            OperationError: If formatting fails.

        Examples:
            >>> formatter = DateTimeFormatter('en-US', date_style='medium',
            ...                              time_style='none')
            >>> start = datetime(2025, 1, 3)
            >>> end = datetime(2025, 1, 5)
            >>> formatter.format_range(start, end)
            'Jan 3 – 5, 2025'
        """
        # Create interval formatter with same style
        # For date intervals, we typically don't want time
        if self._time_style == "none" or self._date_style == "none":
            skeleton = "yMMMd"  # Year, month, day
        else:
            skeleton = "yMMMdjm"  # Include time

        dtifmt = icu.DateIntervalFormat.createInstance(skeleton, self._locale._icu_locale)

        # Convert datetimes to ICU UDate format
        start_cal = icu.GregorianCalendar()
        start_cal.set(start.year, start.month - 1, start.day, start.hour, start.minute, start.second)

        end_cal = icu.GregorianCalendar()
        end_cal.set(end.year, end.month - 1, end.day, end.hour, end.minute, end.second)

        # Format the interval
        interval = icu.DateInterval(start_cal.getTime(), end_cal.getTime())
        return dtifmt.format(interval)

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
        if isinstance(locale, str):
            try:
                locale = Locale(locale)
            except Exception as e:
                msg = f"Invalid locale '{locale}': {e}"
                raise OperationError(msg) from e

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
            if hasattr(self._formatter, 'setRoundingMode'):
                self._formatter.setRoundingMode(rounding_map[rounding_mode])

    def format(self, number: int | float) -> str:
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

    def format_currency(self, amount: int | float, currency: str) -> str:
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
        try:
            currency_unit = icu.CurrencyUnit(currency)
            currency_formatter.setCurrency(currency_unit)
        except Exception:
            # If currency setting fails, format without specific currency
            pass

        return currency_formatter.format(amount)

    def format_compact(self, number: int | float, notation: str = "short") -> str:
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
        except Exception as e:
            # Fallback to regular formatting if compact not available
            return self.format(number)

    def format_range(self, start: int | float, end: int | float) -> str:
        """Format a number range.

        Args:
            start: Start of the range.
            end: End of the range.

        Examples:
            >>> formatter = NumberFormatter('en-US')
            >>> formatter.format_range(10, 20)
            '10–20'

            >>> formatter = NumberFormatter('de-DE', style='currency')
            >>> formatter.format_range(10.50, 25.75, 'EUR')
            '10,50 €–25,75 €'
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
                return f"{start_formatted}–{end_formatted}"
            elif self._style == "percent":
                range_formatter = range_formatter.numberFormatterBoth(
                    icu.NumberFormatter.withLocale(self._locale._icu_locale).unit(icu.MeasureUnit.forIdentifier("percent"))
                )
            
            return range_formatter.formatFormattableRange(start, end).toString()
        except Exception:
            # Fallback to simple range formatting
            start_formatted = self.format(start)
            end_formatted = self.format(end)
            return f"{start_formatted}–{end_formatted}"

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
        if isinstance(locale, str):
            try:
                locale = Locale(locale)
            except Exception as e:
                msg = f"Invalid locale '{locale}': {e}"
                raise OperationError(msg) from e

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
        try:
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

            self._formatter = icu.ListFormatter.createInstance(
                locale._icu_locale, type_map[list_type], style_map[style]
            )
        except Exception as e:
            # Fallback to creating a basic formatter
            try:
                self._formatter = icu.ListFormatter.createInstance(locale._icu_locale)
            except Exception as e2:
                msg = f"Failed to create list formatter: {e2}"
                raise ConfigurationError(msg) from e2

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

        try:
            # Convert to ICU string list
            string_list = [str(item) for item in items]
            return self._formatter.format(string_list)
        except Exception as e:
            # Fallback to simple formatting based on list type and locale
            return self._format_fallback(items)

    def _format_fallback(self, items: list[str]) -> str:
        """Fallback list formatting when ICU formatter fails."""
        if not items:
            return ""

        if len(items) == 1:
            return items[0]

        # Simple fallback based on locale and type
        locale_tag = self._locale.language_tag.lower()
        
        if len(items) == 2:
            # Two items - use appropriate conjunction
            if self._list_type == "or":
                if locale_tag.startswith("es"):
                    return f"{items[0]} o {items[1]}"
                elif locale_tag.startswith("fr"):
                    return f"{items[0]} ou {items[1]}"
                elif locale_tag.startswith("de"):
                    return f"{items[0]} oder {items[1]}"
                else:  # Default to English
                    return f"{items[0]} or {items[1]}"
            else:  # "and" or "units"
                if locale_tag.startswith("es"):
                    return f"{items[0]} y {items[1]}"
                elif locale_tag.startswith("fr"):
                    return f"{items[0]} et {items[1]}"
                elif locale_tag.startswith("de"):
                    return f"{items[0]} und {items[1]}"
                else:  # Default to English
                    return f"{items[0]} and {items[1]}"
        else:
            # Multiple items - use comma separation with final conjunction
            if self._list_type == "or":
                if locale_tag.startswith("es"):
                    return f"{', '.join(items[:-1])} o {items[-1]}"
                elif locale_tag.startswith("fr"):
                    return f"{', '.join(items[:-1])} ou {items[-1]}"
                elif locale_tag.startswith("de"):
                    return f"{', '.join(items[:-1])} oder {items[-1]}"
                else:  # Default to English
                    return f"{', '.join(items[:-1])}, or {items[-1]}"
            else:  # "and" or "units"
                if locale_tag.startswith("es"):
                    return f"{', '.join(items[:-1])} y {items[-1]}"
                elif locale_tag.startswith("fr"):
                    return f"{', '.join(items[:-1])} et {items[-1]}"
                elif locale_tag.startswith("de"):
                    return f"{', '.join(items[:-1])} und {items[-1]}"
                else:  # Default to English
                    return f"{', '.join(items[:-1])}, and {items[-1]}"

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
            f"ListFormatter(locale='{self._locale.language_tag}', "
            f"list_type='{self._list_type}', style='{self._style}')"
        )

