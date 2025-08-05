---
# this_file: src_docs/md/guide/date-time-formatting.md
title: Date-Time Formatting
description: Locale-aware date and time presentation
---

# Date-Time Formatting

UICU provides comprehensive locale-aware date and time formatting, following cultural conventions for displaying temporal information.

## Basic Date Formatting

```python
import uicu
from datetime import datetime, date

# Current date
today = date.today()
now = datetime.now()

# Different locales, same date
locales = ['en-US', 'en-GB', 'de-DE', 'fr-FR', 'ja-JP', 'ar-SA']

for locale_id in locales:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_date_formatter(style='medium')
    formatted = formatter.format(today)
    print(f"{locale.display_name:20}: {formatted}")
```

## Date Format Styles

```python
# Different format styles
styles = ['short', 'medium', 'long', 'full']
locale = uicu.Locale('en-US')

for style in styles:
    formatter = locale.get_date_formatter(style=style)
    formatted = formatter.format(today)
    print(f"{style:8}: {formatted}")
```

## Time Formatting

```python
# Time formatting with different styles
time_styles = ['short', 'medium', 'long', 'full']
locale = uicu.Locale('en-US')

for style in time_styles:
    formatter = locale.get_time_formatter(style=style)
    formatted = formatter.format(now)
    print(f"{style:8}: {formatted}")
```

## Combined Date-Time Formatting

```python
# Combined date and time
locale = uicu.Locale('de-DE')
dt_formatter = locale.get_datetime_formatter(
    date_style='full',
    time_style='short'
)
formatted = dt_formatter.format(now)
print(f"German: {formatted}")
```

## Custom Format Patterns

```python
# Custom format patterns
patterns = [
    'yyyy-MM-dd',           # ISO date
    'dd.MM.yyyy',           # European format
    'MMM d, yyyy',          # Month abbreviation
    'EEEE, MMMM d, yyyy',   # Full day and month names
    'HH:mm:ss',             # 24-hour time
    'h:mm a',               # 12-hour with AM/PM
]

locale = uicu.Locale('en-US')
for pattern in patterns:
    formatter = locale.get_custom_formatter(pattern)
    result = formatter.format(now)
    print(f"{pattern:20}: {result}")
```

## Relative Date Formatting

```python
from datetime import timedelta

# Relative dates
relative_formatter = uicu.RelativeDateFormatter('en-US')

dates = [
    now - timedelta(days=1),    # Yesterday
    now,                        # Today
    now + timedelta(days=1),    # Tomorrow
    now + timedelta(weeks=1),   # Next week
]

for dt in dates:
    relative = relative_formatter.format(dt, reference=now)
    print(f"{dt.strftime('%Y-%m-%d')}: {relative}")
```

## Calendar Systems

```python
# Different calendar systems
calendars = [
    ('en-US', 'gregorian'),
    ('ar-SA', 'islamic'),
    ('he-IL', 'hebrew'),
    ('th-TH', 'buddhist'),
    ('ja-JP', 'japanese'),
]

for locale_id, calendar_type in calendars:
    locale = uicu.Locale(locale_id)
    formatter = locale.get_date_formatter(
        style='long',
        calendar=calendar_type
    )
    formatted = formatter.format(today)
    print(f"{calendar_type:12} ({locale_id}): {formatted}")
```

Continue to [Best Practices](best-practices.md) →