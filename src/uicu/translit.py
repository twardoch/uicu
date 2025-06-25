#!/usr/bin/env python
# this_file: src/uicu/translit.py
"""Script conversion and text transforms.

This module provides Pythonic interfaces for ICU's transliteration functionality,
enabling script conversion and various text transformations.
"""

import icu

from uicu.exceptions import ConfigurationError, OperationError


class Transliterator:
    """Reusable transliterator for better performance.

    This class wraps ICU's Transliterator to provide script conversion
    and text transformation capabilities.
    """

    def __init__(self, transform_id: str, direction: str = "forward"):
        """Create transliterator.

        Args:
            transform_id: ICU transform ID (e.g., 'Greek-Latin', 'Any-NFD').
            direction: 'forward' or 'reverse'.

        Raises:
            ConfigurationError: If transform ID is invalid or creation fails.
        """
        # Map direction string to ICU constant
        if direction == "forward":
            icu_direction = icu.UTransDirection.FORWARD
        elif direction == "reverse":
            icu_direction = icu.UTransDirection.REVERSE
        else:
            msg = f"Invalid direction '{direction}'. Must be 'forward' or 'reverse'."
            raise ConfigurationError(msg)

        # Create ICU transliterator - let ICU errors propagate
        self._transliterator = icu.Transliterator.createInstance(transform_id, icu_direction)

        # Store configuration
        self._transform_id = transform_id
        self._direction = direction

    def transliterate(self, text: str, filter_fn=None) -> str:
        """Apply transliteration to text.

        Args:
            text: Input text to transform.
            filter_fn: Optional function to filter which characters to transliterate.
                      Should take a single character and return True to transliterate.

        Returns:
            Transformed text.
        """
        if filter_fn is None:
            # ICU transliterate modifies the string in-place if using UnicodeString
            # But with Python strings, it returns a new string
            return self._transliterator.transliterate(text)
        # Apply transliteration selectively
        result = []
        for char in text:
            if filter_fn(char):
                result.append(self._transliterator.transliterate(char))
            else:
                result.append(char)
        return "".join(result)

    def __call__(self, text: str) -> str:
        """Make transliterator callable.

        Args:
            text: Input text to transform.

        Returns:
            Transformed text.
        """
        return self.transliterate(text)

    def inverse(self) -> "Transliterator":
        """Return inverse transliterator.

        Returns:
            New Transliterator instance for reverse transformation.

        Raises:
            ConfigurationError: If inverse is not available.
        """
        # Create inverse transliterator
        inverse_trans = self._transliterator.createInverse()

        # Wrap in new Transliterator instance
        # We need to create a new instance that wraps the inverse
        new_instance = object.__new__(Transliterator)
        new_instance._transliterator = inverse_trans
        new_instance._transform_id = f"{self._transform_id}_inverse"
        new_instance._direction = "reverse" if self._direction == "forward" else "forward"

        return new_instance

    @classmethod
    def from_rules(cls, name: str, rules: str, direction: str = "forward") -> "Transliterator":
        """Create transliterator from custom rules.

        Args:
            name: Name for the custom transliterator.
            rules: Transliteration rules in ICU syntax.
            direction: 'forward' or 'reverse'.

        Returns:
            New Transliterator instance.

        Raises:
            ConfigurationError: If rules are invalid.
        """
        # Map direction string to ICU constant
        if direction == "forward":
            icu_direction = icu.UTransDirection.FORWARD
        elif direction == "reverse":
            icu_direction = icu.UTransDirection.REVERSE
        else:
            msg = f"Invalid direction '{direction}'. Must be 'forward' or 'reverse'."
            raise ConfigurationError(msg)

        # Create transliterator from rules
        icu_trans = icu.Transliterator.createFromRules(name, rules, icu_direction)

        # Wrap in new Transliterator instance
        new_instance = object.__new__(cls)
        new_instance._transliterator = icu_trans
        new_instance._transform_id = name
        new_instance._direction = direction

        return new_instance

    @property
    def transform_id(self) -> str:
        """The transform ID of this transliterator."""
        return self._transform_id

    @property
    def id(self) -> str:
        """Alias for transform_id for compatibility."""
        return self._transform_id

    @property
    def direction(self) -> str:
        """The direction of this transliterator."""
        return self._direction

    @property
    def display_name(self) -> str:
        """Human-readable name of the transliterator."""
        try:
            # PyICU transliterators have getDisplayName method
            return self._transliterator.getDisplayName(icu.Locale.getDefault())
        except AttributeError:
            # Fallback to transform ID
            return self._transform_id

    @property
    def source_set(self) -> set[str] | None:
        """The set of characters that this transliterator will transform."""
        try:
            # PyICU transliterators may have getSourceSet method
            uset = self._transliterator.getSourceSet()
            if uset:
                # Convert UnicodeSet to Python set
                return {uset.charAt(i) for i in range(uset.size())}
        except (AttributeError, Exception):
            pass
        return None

    @property
    def target_set(self) -> set[str] | None:
        """The set of characters that this transliterator can produce."""
        try:
            # PyICU transliterators may have getTargetSet method
            uset = self._transliterator.getTargetSet()
            if uset:
                # Convert UnicodeSet to Python set
                return {uset.charAt(i) for i in range(uset.size())}
        except (AttributeError, Exception):
            pass
        return None

    def has_inverse(self) -> bool:
        """Check if this transliterator has an inverse transform."""
        try:
            # Try to create inverse - if it succeeds, inverse exists
            self._transliterator.createInverse()
            return True
        except Exception:
            return False

    def get_inverse(self) -> "Transliterator":
        """Get the inverse transliterator.

        This is an alias for the inverse() method.
        """
        return self.inverse()

    def __repr__(self) -> str:
        """Return representation."""
        return f"Transliterator('{self._transform_id}', direction='{self._direction}')"


# Convenience functions


def transliterate(text: str, transform_id: str, direction: str = "forward", filter_fn=None) -> str:
    """Apply transliteration transform.

    This is a convenience function that creates a temporary transliterator
    for one-off transformations.

    Args:
        text: Input text to transform.
        transform_id: ICU transform ID (e.g., 'Greek-Latin', 'Any-NFD').
        direction: 'forward' or 'reverse'.
        filter_fn: Optional function to filter which characters to transliterate.

    Returns:
        Transformed text.

    Example:
        >>> transliterate('Ελληνικά', 'Greek-Latin')
        'Ellēniká'
        >>> transliterate('北京', 'Han-Latin')
        'běi jīng'
    """
    trans = Transliterator(transform_id, direction)
    return trans.transliterate(text, filter_fn=filter_fn)


def get_available_transforms() -> list[str]:
    """Return list of available transform IDs.

    Returns:
        List of available ICU transform identifiers.
    """
    # Get available IDs from ICU
    # ICU returns an Enumeration, convert to list
    ids = []
    enumeration = icu.Transliterator.getAvailableIDs()

    # Iterate through enumeration
    while True:
        try:
            # Get next ID
            transform_id = enumeration.next()
            if transform_id is None:
                break
            ids.append(str(transform_id))
        except StopIteration:
            break

    return sorted(ids)


def list_transform_aliases(transform_id: str) -> list[str]:
    """Get aliases for a transform ID.

    Args:
        transform_id: Transform ID to get aliases for.

    Returns:
        List of alias IDs that map to the same transform.
    """
    try:
        # ICU doesn't directly expose aliases, but we can check
        # which IDs create equivalent transliterators
        aliases = []
        base_trans = icu.Transliterator.createInstance(transform_id)

        for test_id in get_available_transforms():
            if test_id != transform_id:
                try:
                    test_trans = icu.Transliterator.createInstance(test_id)
                    # Compare by ID (not perfect but reasonable)
                    if test_trans.getID() == base_trans.getID():
                        aliases.append(test_id)
                except Exception:
                    pass

        return aliases
    except Exception as e:
        msg = f"Failed to get aliases for '{transform_id}': {e}"
        raise ConfigurationError(msg) from e


def find_transforms(keyword: str) -> list[str]:
    """Find transform IDs containing a keyword.

    Useful for discovering available transforms for a script or language.

    Args:
        keyword: Search term (case-insensitive).

    Returns:
        List of matching transform IDs.

    Example:
        >>> find_transforms('cyrillic')
        ['Any-Cyrillic', 'Cyrillic-Latin', 'Latin-Cyrillic', ...]
        >>> find_transforms('arabic')
        ['Any-Arabic', 'Arabic-Latin', 'Latin-Arabic', ...]
    """
    keyword_lower = keyword.lower()
    transforms = get_available_transforms()
    return [t for t in transforms if keyword_lower in t.lower()]
