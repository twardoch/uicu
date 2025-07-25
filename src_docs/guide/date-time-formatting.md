# Date/Time Formatting

UICU provides locale-aware date and time formatting that respects cultural conventions for displaying dates, times, and intervals. This ensures your application shows dates and times in formats familiar to users worldwide.

## Understanding Date/Time Formatting

Different cultures format dates and times differently:
- **US**: 12/31/2024 (MM/DD/YYYY), 3:30 PM
- **Europe**: 31.12.2024 (DD.MM.YYYY), 15:30
- **ISO**: 2024-12-31, 15:30:00
- **Japanese**: 2024年12月31日, 15時30分

```python
import uicu
from datetime import datetime

# Same datetime, different locales
dt = datetime(2024, 12, 31, 15, 30, 0)

locales = ['en-US', 'de-DE', 'ja-JP', 'ar-SA']
for locale_id in locales:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_datetime_formatter()
    formatted = formatter.format(dt)
    print(f"{locale_id}: {formatted}")
```

## Basic Date/Time Formatting

### Creating Formatters

```python
from datetime import datetime, timezone

# Create formatters different ways
# 1. From locale
locale = uicu.Locale('en-US')
formatter1 = locale.get_datetime_formatter()

# 2. With specific locale
formatter2 = uicu.DateTimeFormatter('fr-FR')

# 3. With style options
formatter3 = uicu.DateTimeFormatter(
    'en-US',
    date_style='full',
    time_style='short'
)

# Format current time
now = datetime.now()
print(f"Default: {formatter1.format(now)}")
print(f"French: {formatter2.format(now)}")
print(f"Full/Short: {formatter3.format(now)}")
```

### Format Styles

UICU supports four standard styles for dates and times:

```python
dt = datetime(2024, 12, 31, 15, 30, 45)
styles = ['short', 'medium', 'long', 'full']

# Date styles
print("Date styles (en-US):")
for style in styles:
    formatter = uicu.DateTimeFormatter('en-US', date_style=style)
    print(f"  {style:8} {formatter.format(dt)}")

print("\nTime styles (en-US):")
for style in styles:
    formatter = uicu.DateTimeFormatter('en-US', time_style=style)
    print(f"  {style:8} {formatter.format(dt)}")

# Combined styles
print("\nCombined date and time:")
formatter = uicu.DateTimeFormatter('en-US', date_style='long', time_style='short')
print(f"  {formatter.format(dt)}")
```

## Locale-Specific Formatting

### Different Locale Conventions

```python
dt = datetime(2024, 12, 31, 15, 30, 0)

# Test various locales
test_locales = [
    ('en-US', 'US English'),
    ('en-GB', 'British English'),
    ('de-DE', 'German'),
    ('fr-FR', 'French'),
    ('es-ES', 'Spanish'),
    ('it-IT', 'Italian'),
    ('ja-JP', 'Japanese'),
    ('zh-CN', 'Chinese'),
    ('ar-SA', 'Arabic'),
    ('ru-RU', 'Russian'),
]

print("Date formatting across locales:")
for locale_id, name in test_locales:
    formatter = uicu.DateTimeFormatter(locale_id, date_style='full')
    formatted = formatter.format(dt)
    print(f"{name:15} {formatted}")
```

### Time Zones

```python
from datetime import timezone, timedelta

# Create datetime with timezone
utc_dt = datetime(2024, 12, 31, 20, 30, 0, tzinfo=timezone.utc)

# Format with timezone information
locales_with_tz = [
    ('en-US', 'America/New_York'),
    ('de-DE', 'Europe/Berlin'),
    ('ja-JP', 'Asia/Tokyo'),
    ('au-AU', 'Australia/Sydney'),
]

for locale_id, tz_name in locales_with_tz:
    formatter = uicu.DateTimeFormatter(
        locale_id,
        date_style='medium',
        time_style='long'
    )
    formatted = formatter.format(utc_dt, tz=tz_name)
    print(f"{locale_id} ({tz_name:20}): {formatted}")
```

## Pattern-Based Formatting

### Using Custom Patterns

```python
# Create formatter with custom pattern
patterns = [
    ("yyyy-MM-dd", "ISO date"),
    ("dd/MM/yyyy", "European style"),
    ("MMM d, yyyy", "US style abbreviated"),
    ("EEEE, MMMM d, yyyy", "Full day and month"),
    ("yyyy年MM月dd日", "Japanese style"),
    ("h:mm a", "12-hour time"),
    ("HH:mm:ss", "24-hour time with seconds"),
    ("yyyy-MM-dd'T'HH:mm:ss", "ISO 8601"),
]

dt = datetime(2024, 12, 31, 15, 30, 45)

print("Pattern-based formatting:")
for pattern, desc in patterns:
    formatter = uicu.DateTimeFormatter('en-US', pattern=pattern)
    formatted = formatter.format(dt)
    print(f"{desc:25} {pattern:25} → {formatted}")
```

### Pattern Components

```python
# Common pattern components
dt = datetime(2024, 12, 31, 15, 30, 45)

components = [
    # Years
    ("y", "Year (minimum digits)"),
    ("yy", "2-digit year"),
    ("yyyy", "4-digit year"),
    
    # Months
    ("M", "Month (minimum digits)"),
    ("MM", "2-digit month"),
    ("MMM", "Abbreviated month"),
    ("MMMM", "Full month name"),
    
    # Days
    ("d", "Day (minimum digits)"),
    ("dd", "2-digit day"),
    
    # Weekdays
    ("E", "Abbreviated weekday"),
    ("EEEE", "Full weekday name"),
    
    # Hours
    ("h", "12-hour (minimum)"),
    ("hh", "12-hour (2-digit)"),
    ("H", "24-hour (minimum)"),
    ("HH", "24-hour (2-digit)"),
    
    # Others
    ("a", "AM/PM"),
    ("z", "Timezone abbreviation"),
    ("zzzz", "Timezone full name"),
]

print("Pattern components:")
for pattern, desc in components:
    try:
        formatter = uicu.DateTimeFormatter('en-US', pattern=pattern)
        formatted = formatter.format(dt)
        print(f"{pattern:8} {desc:30} → {formatted}")
    except Exception as e:
        print(f"{pattern:8} {desc:30} → Error: {e}")
```

## Practical Examples

### User-Friendly Date Display

```python
class DateDisplayer:
    """Display dates in user-friendly formats."""
    
    def __init__(self, locale='en-US'):
        self.locale = uicu.Locale(locale)
        
        # Create various formatters
        self.formatters = {
            'full': self.locale.get_datetime_formatter(date_style='full'),
            'long': self.locale.get_datetime_formatter(date_style='long'),
            'medium': self.locale.get_datetime_formatter(date_style='medium'),
            'short': self.locale.get_datetime_formatter(date_style='short'),
            'time_only': self.locale.get_datetime_formatter(time_style='short'),
            'date_only': self.locale.get_datetime_formatter(date_style='medium'),
        }
    
    def format_for_display(self, dt, context='medium'):
        """Format datetime based on context."""
        if context in self.formatters:
            return self.formatters[context].format(dt)
        return self.formatters['medium'].format(dt)
    
    def format_relative(self, dt):
        """Format relative to current time (simple implementation)."""
        now = datetime.now()
        delta = now - dt
        
        if delta.days == 0:
            return f"Today at {self.formatters['time_only'].format(dt)}"
        elif delta.days == 1:
            return f"Yesterday at {self.formatters['time_only'].format(dt)}"
        elif delta.days < 7:
            weekday_formatter = uicu.DateTimeFormatter(
                self.locale.language_tag,
                pattern='EEEE'
            )
            weekday = weekday_formatter.format(dt)
            time = self.formatters['time_only'].format(dt)
            return f"{weekday} at {time}"
        else:
            return self.formatters['medium'].format(dt)

# Example usage
displayer = DateDisplayer('en-US')
now = datetime.now()
dates = [
    now,
    now - timedelta(hours=3),
    now - timedelta(days=1),
    now - timedelta(days=3),
    now - timedelta(days=30),
]

print("User-friendly date display:")
for dt in dates:
    print(f"  {displayer.format_relative(dt)}")
```

### Multi-Format Date Input/Output

```python
class DateFormatter:
    """Handle multiple date formats for input/output."""
    
    def __init__(self, locale='en-US'):
        self.locale = locale
        
        # Output formats
        self.output_formats = {
            'display': uicu.DateTimeFormatter(locale, date_style='long'),
            'edit': uicu.DateTimeFormatter(locale, pattern='yyyy-MM-dd'),
            'api': uicu.DateTimeFormatter(locale, pattern="yyyy-MM-dd'T'HH:mm:ss"),
            'filename': uicu.DateTimeFormatter(locale, pattern='yyyyMMdd_HHmmss'),
        }
    
    def format(self, dt, format_type='display'):
        """Format date for specific use case."""
        if format_type in self.output_formats:
            return self.output_formats[format_type].format(dt)
        return str(dt)
    
    def format_all(self, dt):
        """Show all format variations."""
        results = {}
        for name, formatter in self.output_formats.items():
            results[name] = formatter.format(dt)
        return results

# Example
formatter = DateFormatter('en-US')
dt = datetime(2024, 12, 31, 15, 30, 45)

print("Date in different formats:")
for format_type, formatted in formatter.format_all(dt).items():
    print(f"  {format_type:10} {formatted}")

# Practical uses
print(f"\nDisplay to user: {formatter.format(dt, 'display')}")
print(f"Edit field: {formatter.format(dt, 'edit')}")
print(f"API response: {formatter.format(dt, 'api')}")
print(f"Filename: report_{formatter.format(dt, 'filename')}.pdf")
```

### Appointment Scheduler

```python
class AppointmentScheduler:
    """Schedule appointments with locale-aware formatting."""
    
    def __init__(self, locale='en-US'):
        self.locale = uicu.Locale(locale)
        
        # Formatters for different contexts
        self.date_formatter = uicu.DateTimeFormatter(
            locale,
            pattern='EEEE, MMMM d, yyyy'
        )
        self.time_formatter = uicu.DateTimeFormatter(
            locale,
            pattern='h:mm a'
        )
        self.confirmation_formatter = self.locale.get_datetime_formatter(
            date_style='full',
            time_style='short'
        )
    
    def format_appointment(self, dt, duration_minutes=60):
        """Format appointment details."""
        end_time = dt + timedelta(minutes=duration_minutes)
        
        date_str = self.date_formatter.format(dt)
        start_str = self.time_formatter.format(dt)
        end_str = self.time_formatter.format(end_time)
        
        return {
            'date': date_str,
            'time': f"{start_str} - {end_str}",
            'duration': f"{duration_minutes} minutes",
            'confirmation': self.confirmation_formatter.format(dt)
        }
    
    def format_reminder(self, dt):
        """Format appointment reminder."""
        now = datetime.now()
        days_until = (dt.date() - now.date()).days
        
        if days_until == 0:
            return f"Today at {self.time_formatter.format(dt)}"
        elif days_until == 1:
            return f"Tomorrow at {self.time_formatter.format(dt)}"
        else:
            return f"In {days_until} days: {self.confirmation_formatter.format(dt)}"

# Example usage
scheduler = AppointmentScheduler('en-US')

# Schedule appointments
appointments = [
    datetime.now() + timedelta(hours=3),
    datetime.now() + timedelta(days=1, hours=10),
    datetime.now() + timedelta(days=7, hours=14),
]

print("Appointment Schedule:")
for appt in appointments:
    details = scheduler.format_appointment(appt, 45)
    print(f"\n{details['date']}")
    print(f"  Time: {details['time']}")
    print(f"  Duration: {details['duration']}")
    print(f"  Reminder: {scheduler.format_reminder(appt)}")
```

### International Event Coordinator

```python
class EventCoordinator:
    """Coordinate international events with multiple timezones."""
    
    def __init__(self):
        self.locations = {
            'New York': ('en-US', 'America/New_York'),
            'London': ('en-GB', 'Europe/London'),
            'Tokyo': ('ja-JP', 'Asia/Tokyo'),
            'Sydney': ('en-AU', 'Australia/Sydney'),
            'Dubai': ('ar-AE', 'Asia/Dubai'),
        }
    
    def format_event_times(self, event_utc):
        """Show event time in multiple locations."""
        results = []
        
        for city, (locale_id, tz) in self.locations.items():
            formatter = uicu.DateTimeFormatter(
                locale_id,
                date_style='medium',
                time_style='short'
            )
            
            local_time = formatter.format(event_utc, tz=tz)
            results.append({
                'city': city,
                'local_time': local_time,
                'timezone': tz
            })
        
        return results
    
    def create_invitation(self, event_name, event_utc):
        """Create multilingual event invitation."""
        print(f"Event: {event_name}")
        print(f"UTC Time: {event_utc}")
        print("\nLocal Times:")
        
        times = self.format_event_times(event_utc)
        for info in times:
            print(f"  {info['city']:10} {info['local_time']}")

# Example
coordinator = EventCoordinator()
event_time = datetime(2024, 12, 31, 20, 0, 0, tzinfo=timezone.utc)
coordinator.create_invitation("Global New Year's Celebration", event_time)
```

## Working with Different Calendars

```python
# Note: Full calendar support requires additional ICU configuration
# This shows the concept

def format_in_calendar(dt, locale_id, calendar_type=None):
    """Format date in specific calendar system."""
    # Standard Gregorian calendar
    formatter = uicu.DateTimeFormatter(locale_id, date_style='full')
    
    # Some locales have default non-Gregorian calendars
    if locale_id == 'ja-JP' and calendar_type == 'japanese':
        # Japanese imperial calendar
        formatter = uicu.DateTimeFormatter('ja-JP-u-ca-japanese', date_style='full')
    elif locale_id == 'th-TH' and calendar_type == 'buddhist':
        # Buddhist calendar
        formatter = uicu.DateTimeFormatter('th-TH-u-ca-buddhist', date_style='full')
    
    return formatter.format(dt)

# Example
dt = datetime(2024, 12, 31)
calendars = [
    ('en-US', None, 'Gregorian'),
    ('ja-JP', 'japanese', 'Japanese Imperial'),
    ('th-TH', 'buddhist', 'Buddhist'),
]

print("Different calendar systems:")
for locale_id, cal_type, cal_name in calendars:
    try:
        formatted = format_in_calendar(dt, locale_id, cal_type)
        print(f"{cal_name:20} {formatted}")
    except Exception as e:
        print(f"{cal_name:20} Not available")
```

## Performance Considerations

### Reuse Formatters

```python
import time

# Comparison: creating formatters vs reusing
iterations = 10000
dt = datetime.now()

# Method 1: Create new formatter each time
start = time.time()
for _ in range(iterations):
    formatter = uicu.DateTimeFormatter('en-US')
    result = formatter.format(dt)
slow_time = time.time() - start

# Method 2: Reuse formatter
formatter = uicu.DateTimeFormatter('en-US')
start = time.time()
for _ in range(iterations):
    result = formatter.format(dt)
fast_time = time.time() - start

print(f"Create each time: {slow_time:.3f}s")
print(f"Reuse formatter: {fast_time:.3f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

### Caching Formatters

```python
class FormatterCache:
    """Cache formatters for performance."""
    
    def __init__(self):
        self._cache = {}
    
    def get_formatter(self, locale_id, **kwargs):
        """Get or create cached formatter."""
        # Create cache key
        key = (locale_id, tuple(sorted(kwargs.items())))
        
        if key not in self._cache:
            self._cache[key] = uicu.DateTimeFormatter(locale_id, **kwargs)
        
        return self._cache[key]
    
    def format(self, dt, locale_id, **kwargs):
        """Format using cached formatter."""
        formatter = self.get_formatter(locale_id, **kwargs)
        return formatter.format(dt)

# Example usage
cache = FormatterCache()
dt = datetime.now()

# These will reuse cached formatters
for _ in range(5):
    print(cache.format(dt, 'en-US', date_style='full'))
    print(cache.format(dt, 'fr-FR', date_style='medium', time_style='short'))
```

## Common Patterns

### ISO 8601 Formatting

```python
def format_iso8601(dt, include_timezone=True):
    """Format datetime as ISO 8601."""
    if include_timezone:
        pattern = "yyyy-MM-dd'T'HH:mm:ssXXX"
    else:
        pattern = "yyyy-MM-dd'T'HH:mm:ss"
    
    formatter = uicu.DateTimeFormatter('en-US', pattern=pattern)
    return formatter.format(dt)

# Examples
dt_naive = datetime(2024, 12, 31, 15, 30, 45)
dt_aware = datetime(2024, 12, 31, 15, 30, 45, tzinfo=timezone.utc)

print(f"Naive: {format_iso8601(dt_naive, include_timezone=False)}")
print(f"UTC: {format_iso8601(dt_aware, include_timezone=True)}")
```

### Relative Time Formatting (Simple)

```python
def format_relative_time(dt, locale_id='en-US'):
    """Simple relative time formatting."""
    now = datetime.now()
    if dt.tzinfo:
        now = now.replace(tzinfo=dt.tzinfo)
    
    delta = now - dt
    
    # Time formatter for today/yesterday
    time_formatter = uicu.DateTimeFormatter(locale_id, time_style='short')
    
    if delta.days == 0:
        if delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago" if minutes > 1 else "just now"
        else:
            return f"Today at {time_formatter.format(dt)}"
    elif delta.days == 1:
        return f"Yesterday at {time_formatter.format(dt)}"
    elif delta.days < 7:
        weekday_formatter = uicu.DateTimeFormatter(locale_id, pattern='EEEE')
        return weekday_formatter.format(dt)
    else:
        date_formatter = uicu.DateTimeFormatter(locale_id, date_style='medium')
        return date_formatter.format(dt)

# Test
now = datetime.now()
test_times = [
    now - timedelta(minutes=5),
    now - timedelta(hours=2),
    now - timedelta(days=1, hours=3),
    now - timedelta(days=4),
    now - timedelta(days=30),
]

print("Relative times:")
for dt in test_times:
    print(f"  {format_relative_time(dt)}")
```

## Best Practices

1. **Always specify locale** - Don't rely on system defaults
2. **Reuse formatters** - They're expensive to create
3. **Use appropriate styles** - Match user expectations
4. **Handle timezones properly** - Especially for international apps
5. **Test with various locales** - Date formats vary significantly
6. **Consider context** - Different formats for display vs. editing
7. **Cache formatters** - For high-performance applications

## Future Features (v2.0)

The following features are planned for UICU v2.0:
- Date/time parsing
- Relative time formatting ("3 days ago")
- Duration formatting
- Date intervals
- Custom calendar support
- Timezone conversion utilities

## Next Steps

- Review [Best Practices](best-practices.md) for internationalization
- See [Examples](../examples/locale-aware-apps.md) for complete applications
- Explore other [Guide topics](index.md)