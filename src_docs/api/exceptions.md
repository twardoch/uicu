# uicu.exceptions

Exception classes for UICU error handling.

This module defines the exception hierarchy used throughout UICU for error reporting.

## Exception Classes

### `UICUError`

::: uicu.exceptions.UICUError

### `ConfigurationError`

::: uicu.exceptions.ConfigurationError

### `OperationError`

::: uicu.exceptions.OperationError

## Exception Hierarchy

```
Exception
└── UICUError (base UICU exception)
    ├── ConfigurationError (configuration/setup errors)
    └── OperationError (runtime operation errors)
```

## Examples

### Basic Error Handling

```python
import uicu
from uicu.exceptions import UICUError, ConfigurationError, OperationError

# Catch any UICU error
try:
    char = uicu.Char('invalid string with multiple chars')
except UICUError as e:
    print(f"UICU error: {e}")

# Catch specific error types
try:
    locale = uicu.Locale('invalid-locale-tag-xyz')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except OperationError as e:
    print(f"Operation error: {e}")
```

### Configuration Errors

Configuration errors occur during setup or initialization:

```python
from uicu import Collator, DateTimeFormatter
from uicu.exceptions import ConfigurationError

# Invalid locale
try:
    collator = Collator('xyz-invalid')
except ConfigurationError as e:
    print(f"Invalid locale: {e}")

# Invalid collation strength
try:
    collator = Collator('en-US', strength='invalid')
except ConfigurationError as e:
    print(f"Invalid strength: {e}")

# Invalid date style
try:
    formatter = DateTimeFormatter('en-US', date_style='invalid')
except OperationError as e:  # Note: Currently raises OperationError
    print(f"Invalid style: {e}")
```

### Operation Errors

Operation errors occur during runtime operations:

```python
from uicu import Transliterator, Char
from uicu.exceptions import OperationError

# Invalid transliterator
try:
    trans = Transliterator('Invalid-Transform')
except OperationError as e:
    print(f"Invalid transform: {e}")

# Character operation on invalid input
try:
    char = Char('')  # Empty string
except UICUError as e:
    print(f"Invalid character: {e}")
```

### Error Context

UICU exceptions include helpful context:

```python
import uicu

# Detailed error messages
try:
    char = uicu.Char('Hello')  # Multiple characters
except uicu.UICUError as e:
    print(f"Error: {e}")
    # Output: "Character must be a single Unicode character, got 5"

try:
    trans = uicu.Transliterator('NoSuch-Transform')
except uicu.OperationError as e:
    print(f"Error: {e}")
    # Output includes the invalid transform ID
```

## Best Practices

### 1. Catch Specific Exceptions

```python
def process_text(text, locale='en-US'):
    """Process text with proper error handling."""
    try:
        # Try to create locale-specific processor
        collator = uicu.Collator(locale)
        return collator.sort(text.split())
    except ConfigurationError:
        # Fall back to default locale
        print(f"Warning: Invalid locale '{locale}', using default")
        collator = uicu.Collator('en-US')
        return collator.sort(text.split())
    except OperationError as e:
        # Operation failed
        print(f"Error during sorting: {e}")
        return text.split()  # Return unsorted
```

### 2. Provide User-Friendly Messages

```python
def format_date_safe(date, locale='en-US', style='medium'):
    """Format date with user-friendly error handling."""
    try:
        formatter = uicu.DateTimeFormatter(locale, date_style=style)
        return formatter.format(date)
    except ConfigurationError:
        return f"Error: Invalid locale '{locale}'"
    except OperationError:
        return f"Error: Invalid date style '{style}'"
    except Exception as e:
        return f"Error formatting date: {str(e)}"
```

### 3. Validation Before Operations

```python
def validate_locale(locale_id):
    """Validate locale before use."""
    try:
        locale = uicu.Locale(locale_id)
        # Additional validation
        if not locale.language:
            raise ValueError("Locale has no language component")
        return True
    except (ConfigurationError, ValueError) as e:
        print(f"Invalid locale '{locale_id}': {e}")
        return False

# Use validation
if validate_locale(user_locale):
    process_with_locale(user_locale)
else:
    use_default_locale()
```

### 4. Logging Errors

```python
import logging

logger = logging.getLogger(__name__)

def process_with_logging(text, transform):
    """Process text with error logging."""
    try:
        trans = uicu.Transliterator(transform)
        return trans.transliterate(text)
    except ConfigurationError as e:
        logger.error(f"Invalid transform configuration: {transform}", exc_info=True)
        raise
    except OperationError as e:
        logger.warning(f"Transform operation failed: {e}")
        return text  # Return original
    except Exception as e:
        logger.exception("Unexpected error during transliteration")
        raise
```

## Custom Error Handling

### Creating Error Handlers

```python
class ErrorHandler:
    """Centralized error handling for UICU operations."""
    
    def __init__(self, fallback_locale='en-US'):
        self.fallback_locale = fallback_locale
        self.error_count = 0
    
    def handle_locale_error(self, locale_id, error):
        """Handle locale-related errors."""
        self.error_count += 1
        print(f"Locale error for '{locale_id}': {error}")
        return uicu.Locale(self.fallback_locale)
    
    def handle_operation_error(self, operation, error):
        """Handle operation errors."""
        self.error_count += 1
        print(f"Operation '{operation}' failed: {error}")
        return None
    
    def safe_create_collator(self, locale_id):
        """Safely create a collator with fallback."""
        try:
            return uicu.Collator(locale_id)
        except ConfigurationError as e:
            locale = self.handle_locale_error(locale_id, e)
            return uicu.Collator(locale.language_tag)

# Usage
handler = ErrorHandler()
collator = handler.safe_create_collator('invalid-locale')
print(f"Total errors handled: {handler.error_count}")
```

### Retry Logic

```python
import time
from typing import Optional

def retry_operation(func, max_attempts=3, delay=0.1):
    """Retry an operation that might fail."""
    last_error: Optional[Exception] = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except OperationError as e:
            last_error = e
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
    
    raise last_error or OperationError("Operation failed after retries")

# Example usage
def unstable_operation():
    # Simulated unstable operation
    trans = uicu.Transliterator('Complex-Transform')
    return trans.transliterate("test")

try:
    result = retry_operation(unstable_operation)
except OperationError as e:
    print(f"Failed after retries: {e}")
```

## Testing Error Conditions

```python
import pytest
import uicu

def test_char_errors():
    """Test character creation errors."""
    # Empty string
    with pytest.raises(uicu.UICUError):
        uicu.Char('')
    
    # Multiple characters
    with pytest.raises(uicu.UICUError) as exc_info:
        uicu.Char('Hello')
    assert "must be a single Unicode character" in str(exc_info.value)

def test_locale_errors():
    """Test locale errors."""
    # Invalid locale
    with pytest.raises(uicu.ConfigurationError):
        uicu.Locale('xyz-invalid-abc')

def test_transliterator_errors():
    """Test transliterator errors."""
    # Invalid transform
    with pytest.raises(uicu.OperationError):
        uicu.Transliterator('NoSuch-Transform')
```

## See Also

- [API Reference](index.md) - Complete API documentation
- [Best Practices](../guide/best-practices.md) - Error handling patterns
- Python's [exception documentation](https://docs.python.org/3/tutorial/errors.html)