# Issue 102: Implement DateTimeFormatter

## Overview
Implement a locale-aware DateTimeFormatter class in `uicu.format` module that provides Pythonic interfaces to ICU's date and time formatting capabilities.

## Requirements

### Core Functionality
1. Format Python datetime objects according to locale conventions
2. Parse locale-formatted strings back to datetime objects
3. Support all ICU date/time styles (full, long, medium, short, none)
4. Handle custom patterns (both skeleton and explicit)
5. Proper timezone handling with Python tzinfo integration
6. Thread-safe implementation

### API Design

```python
from datetime import datetime
from uicu import Locale
from uicu.format import DateTimeFormatter

# Basic usage
formatter = DateTimeFormatter('en-US')
dt = datetime.now()
formatted = formatter.format(dt)  # "Jan 25, 2025, 3:45 PM"

# With locale object
locale = Locale('fr-FR')
formatter = locale.get_datetime_formatter(date_style='long', time_style='short')
formatted = formatter.format(dt)  # "25 janvier 2025 à 15:45"

# Custom patterns
formatter = DateTimeFormatter('en-US', pattern='EEEE, MMMM d, yyyy')
formatted = formatter.format(dt)  # "Saturday, January 25, 2025"

# Skeleton patterns (flexible)
formatter = DateTimeFormatter('en-US', skeleton='yMMMd')
formatted = formatter.format(dt)  # "Jan 25, 2025"

# Parsing
parsed = formatter.parse("Jan 25, 2025")  # Returns datetime object
```

## Implementation Plan

### 1. Create DateTimeFormatter Class
```python
class DateTimeFormatter:
    def __init__(
        self,
        locale: str | Locale,
        date_style: str = "medium",
        time_style: str = "medium",
        pattern: str | None = None,
        skeleton: str | None = None,
        timezone: str | tzinfo | None = None,
    ):
        """Initialize formatter with locale and style options."""
        
    def format(self, dt: datetime) -> str:
        """Format datetime to string."""
        
    def parse(self, text: str, lenient: bool = False) -> datetime:
        """Parse string to datetime."""
        
    def format_range(self, start: datetime, end: datetime) -> str:
        """Format datetime range (e.g., 'Jan 3-5, 2025')."""
```

### 2. Style Mapping
- Map string styles to ICU constants:
  - 'full' → icu.DateFormat.FULL
  - 'long' → icu.DateFormat.LONG
  - 'medium' → icu.DateFormat.MEDIUM
  - 'short' → icu.DateFormat.SHORT
  - 'none' → icu.DateFormat.NONE

### 3. Pattern Support
- If pattern provided: use icu.SimpleDateFormat
- If skeleton provided: use icu.DateTimePatternGenerator
- Otherwise: use style-based formatting

### 4. Timezone Handling
- Accept Python tzinfo objects
- Convert to ICU TimeZone
- Default to system timezone if not specified
- Preserve timezone information in parsed dates

### 5. Error Handling
- Raise FormattingError for invalid patterns
- Raise FormattingError for unparseable strings
- Provide helpful error messages with context

## Testing Requirements

### Unit Tests
1. Test all style combinations (date_style × time_style)
2. Test with various locales (en-US, fr-FR, ja-JP, ar-SA)
3. Test custom patterns and skeletons
4. Test timezone handling (UTC, local, specific zones)
5. Test parsing with valid and invalid inputs
6. Test date range formatting
7. Test edge cases (leap years, DST transitions)

### Integration Tests
1. Test with Locale.get_datetime_formatter()
2. Test round-trip formatting and parsing
3. Test with non-Gregorian calendars (future)

## Performance Considerations
- Cache SimpleDateFormat instances per pattern
- Reuse pattern generators
- Minimize timezone conversions
- Profile common use cases

## Documentation
- Comprehensive docstrings with examples
- Pattern syntax reference
- Skeleton vs pattern explanation
- Timezone handling guide
- Common formatting recipes

## Future Enhancements
- Relative time formatting ("3 days ago")
- Date interval formatting with custom patterns
- Field position tracking for UI highlighting
- Calendar system support (Islamic, Hebrew, etc.)
- Duration formatting

## Dependencies
- Requires icu.SimpleDateFormat
- Requires icu.DateFormat
- Requires icu.DateTimePatternGenerator
- Should integrate with Python's datetime and zoneinfo modules

## Success Criteria
1. All ICU date/time formatting features accessible
2. Natural Python datetime integration
3. >95% test coverage
4. Performance within 10% of raw PyICU
5. Clear documentation with examples