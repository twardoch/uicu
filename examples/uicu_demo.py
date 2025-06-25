#!/usr/bin/env python3
"""uicu_demo.py - Comprehensive demonstration of uicu capabilities.

This script showcases 12 interesting uses of the uicu library for
Unicode text processing and internationalization.
"""

from datetime import datetime

import uicu


def demo_1_character_exploration():
    """Demo 1: Explore Unicode character properties."""

    # Interesting characters from different scripts
    chars = ["A", "й", "中", "🎉", "ℵ", "½", "א", "🏁"]

    for char in chars:
        info = uicu.Char(char)
        if info.numeric is not None:
            pass
        if info.mirrored:
            pass


def demo_2_multilingual_sorting():
    """Demo 2: Sort names from different cultures correctly."""

    names = [
        "Åberg",
        "Östberg",
        "Mueller",
        "Müller",
        "MacDonald",
        "O'Brien",
        "van der Berg",
        "García",
        "Gutierrez",
    ]

    # Sort with different locale rules
    locale_ids = ["en-US", "de-DE", "sv-SE", "es-ES"]

    for locale_id in locale_ids:
        uicu.Locale(locale_id)
        sorted_names = uicu.sort(names, locale_id)
        for _i, _name in enumerate(sorted_names, 1):
            pass


def demo_3_text_segmentation():
    """Demo 3: Break text into graphemes, words, and sentences."""

    # Text with complex elements
    text = "Hello! 👨‍👩‍👧‍👦 means family. José's café costs $3.50."

    # Grapheme clusters (user-perceived characters)
    list(uicu.graphemes(text))

    # Words
    [w for w in uicu.words(text) if w.strip()]

    # Sentences
    list(uicu.sentences(text))


def demo_4_script_conversion():
    """Demo 4: Convert between writing systems."""

    examples = [
        ("Москва", "Cyrillic-Latin", "Moscow"),
        ("Ελληνικά", "Greek-Latin", "Greek"),
        ("北京市", "Han-Latin", "Beijing"),
        ("こんにちは", "Hiragana-Latin", "Hello (Japanese)"),
        ("مرحبا", "Arabic-Latin", "Hello (Arabic)"),
    ]

    for text, transform, _description in examples:
        try:
            trans = uicu.Transliterator(transform)
            trans.transliterate(text)
        except Exception:
            pass


def demo_5_locale_aware_formatting():
    """Demo 5: Format dates/times for different locales."""

    dt = datetime(2025, 3, 15, 14, 30)

    locales = [
        ("en-US", "US English"),
        ("en-GB", "British English"),
        ("fr-FR", "French"),
        ("de-DE", "German"),
        ("ja-JP", "Japanese"),
        ("ar-SA", "Arabic"),
    ]

    for locale_id, _name in locales:
        locale = uicu.Locale(locale_id)
        formatter = locale.get_datetime_formatter(date_style="long", time_style="short")
        formatter.format(dt)


def demo_6_numeric_collation():
    """Demo 6: Smart numeric sorting."""

    items = [
        "Chapter 2",
        "Chapter 10",
        "Chapter 1",
        "Chapter 21",
        "Chapter 3",
        "Version 2.9",
        "Version 2.10",
        "Version 2.100",
    ]

    # Regular sorting
    regular = uicu.sort(items, "en-US")
    for _item in regular:
        pass

    # Numeric sorting
    numeric = uicu.sort(items, "en-US", numeric=True)
    for _item in numeric:
        pass


def demo_7_text_transformation():
    """Demo 7: Unicode text transformations."""

    original = """Café São Paulo — "naïve" approach"""

    transforms = [
        ("NFC", "Canonical Composition"),
        ("NFD", "Canonical Decomposition"),
        ("NFKC", "Compatibility Composition"),
        ("Latin-ASCII", "Remove Accents"),
        ("Lower", "Lowercase"),
        ("Upper", "Uppercase"),
        ("Title", "Title Case"),
    ]

    for transform_id, _description in transforms:
        uicu.transliterate(original, transform_id)
        if transform_id == "NFD":
            pass


def demo_8_script_detection():
    """Demo 8: Detect the primary script in text."""

    texts = [
        ("Hello, world!", "English"),
        ("Привет, мир!", "Russian"),
        ("你好世界", "Chinese"),
        ("مرحبا بالعالم", "Arabic"),
        ("Γεια σου κόσμε", "Greek"),
        ("שלום עולם", "Hebrew"),
        ("Mixed: Hello, 你好, مرحبا", "Mixed scripts"),
    ]

    for text, _description in texts:
        script = uicu.detect_script(text)
        if script:
            uicu.script_name(script)
        else:
            pass


def demo_9_thai_word_breaking():
    """Demo 9: Word segmentation for languages without spaces."""

    # Thai text without spaces between words
    thai_text = "สวัสดีครับยินดีต้อนรับสู่ประเทศไทย"

    # Segment into words
    words = list(uicu.words(thai_text, locale="th-TH"))
    # Filter out spaces
    words = [w for w in words if w.strip()]

    for _i, _word in enumerate(words, 1):
        pass


def demo_10_emoji_handling():
    """Demo 10: Proper handling of emoji and complex graphemes."""

    # Text with various emoji
    text = "I ❤️ Python! 👨‍💻👩‍💻 Happy coding! 🇺🇸🇬🇧🇫🇷"

    # Count actual graphemes
    graphemes = list(uicu.graphemes(text))

    # Show complex graphemes
    complex_graphemes = [g for g in graphemes if len(g) > 1]
    for g in complex_graphemes:
        [f"U+{ord(c):04X}" for c in g]


def demo_11_case_sensitive_sorting():
    """Demo 11: Control case sensitivity in sorting."""

    words = ["Apple", "apple", "Banana", "banana", "Cherry", "cherry"]

    # Different collation strengths
    strengths = [
        ("primary", "Ignore case and accents"),
        ("secondary", "Consider accents, ignore case"),
        ("tertiary", "Consider case (default)"),
    ]

    for strength, _description in strengths:
        collator = uicu.Collator("en-US", strength=strength)
        sorted_words = collator.sort(words)
        for _word in sorted_words:
            pass


def demo_12_bidirectional_text():
    """Demo 12: Handle mixed-direction text."""

    # Mixed LTR and RTL text
    examples = [
        "Hello שלום World",
        "The price is 123 ₪",
        "مرحبا Python مبرمج",
        "Email: user@example.com בעברית",
    ]

    for text in examples:
        # Analyze character directions
        def get_bidi_description(bidi_class):
            """Get human-readable description for bidirectional class."""
            if bidi_class in ["R", "AL"]:
                return "RTL"
            if bidi_class == "L":
                return "LTR"
            if bidi_class in ["EN", "AN"]:
                return "Number"
            return f"Other ({bidi_class})"

        for char in text:
            if char.strip():
                info = uicu.Char(char)
                bidi = info.bidirectional
                get_bidi_description(bidi)


def main():
    """Run all demonstrations."""

    demos = [
        demo_1_character_exploration,
        demo_2_multilingual_sorting,
        demo_3_text_segmentation,
        demo_4_script_conversion,
        demo_5_locale_aware_formatting,
        demo_6_numeric_collation,
        demo_7_text_transformation,
        demo_8_script_detection,
        demo_9_thai_word_breaking,
        demo_10_emoji_handling,
        demo_11_case_sensitive_sorting,
        demo_12_bidirectional_text,
    ]

    for _i, demo in enumerate(demos, 1):
        demo()
        # Non-interactive mode for scripting


if __name__ == "__main__":
    main()
