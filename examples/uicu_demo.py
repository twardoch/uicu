#!/usr/bin/env python3
"""uicu_demo.py - Comprehensive demonstration of uicu capabilities.

This script showcases 12 interesting uses of the uicu library for
Unicode text processing and internationalization.
"""

from datetime import datetime
import uicu


def demo_1_character_exploration():
    """Demo 1: Explore Unicode character properties."""
    print("=== Demo 1: Unicode Character Exploration ===")

    # Interesting characters from different scripts
    chars = ["A", "й", "中", "🎉", "ℵ", "½", "א", "🏁"]


    for char in chars:
        info = uicu.Char(char)
        print(f"\nCharacter: {char} (U+{ord(char):04X})")
        print(f"  Name: {info.name}")
        print(f"  Category: {info.category}")
        print(f"  Script: {info.script} - {uicu.script_name(info.script)}")
        print(f"  Block: {info.block}")
        if info.numeric is not None:
            print(f"  Numeric Value: {info.numeric}")
        if info.mirrored:
            print(f"  Mirrored: Yes")


def demo_2_multilingual_sorting():
    """Demo 2: Sort names from different cultures correctly."""
    print("\n=== Demo 2: Culture-Aware Name Sorting ===")

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
        locale = uicu.Locale(locale_id)
        sorted_names = uicu.sort(names, locale_id)
        print(f"\n{locale.display_name} sorting:")
        for i, name in enumerate(sorted_names, 1):
            print(f"  {i}. {name}")


def demo_3_text_segmentation():
    """Demo 3: Break text into graphemes, words, and sentences."""
    print("\n=== Demo 3: Text Segmentation ===")

    # Text with complex elements
    text = "Hello! 👨‍👩‍👧‍👦 means family. José's café costs $3.50."

    print(f"\nOriginal text: {text}")

    # Grapheme clusters (user-perceived characters)
    graphemes = list(uicu.graphemes(text))
    print(f"\nGraphemes ({len(graphemes)}): {graphemes[:20]}...")
    print(f"  Note: Family emoji is 1 grapheme: '{graphemes[7]}'")

    # Words
    words = [w for w in uicu.words(text) if w.strip()]
    print(f"\nWords: {words}")

    # Sentences
    sentences = list(uicu.sentences(text))
    print(f"\nSentences: {sentences}")


def demo_4_script_conversion():
    """Demo 4: Convert between writing systems."""
    print("\n=== Demo 4: Script Conversion (Transliteration) ===")

    examples = [
        ("Москва", "Cyrillic-Latin", "Moscow"),
        ("Ελληνικά", "Greek-Latin", "Greek"),
        ("北京市", "Han-Latin", "Beijing"),
        ("こんにちは", "Hiragana-Latin", "Hello (Japanese)"),
        ("مرحبا", "Arabic-Latin", "Hello (Arabic)"),
    ]

    for text, transform, description in examples:
        try:
            trans = uicu.Transliterator(transform)
            result = trans.transliterate(text)
            print(f"\n{description}:")
            print(f"  Original: {text}")
            print(f"  Romanized: {result}")
        except Exception as e:
            print(f"\n{description}:")
            print(f"  Original: {text}")
            print(f"  Error: {e}")


def demo_5_locale_aware_formatting():
    """Demo 5: Format dates/times for different locales."""
    print("\n=== Demo 5: Locale-Aware Date/Time Formatting ===")

    dt = datetime(2025, 3, 15, 14, 30)

    locales = [
        ("en-US", "US English"),
        ("en-GB", "British English"),
        ("fr-FR", "French"),
        ("de-DE", "German"),
        ("ja-JP", "Japanese"),
        ("ar-SA", "Arabic"),
    ]

    for locale_id, name in locales:
        locale = uicu.Locale(locale_id)
        formatter = locale.get_datetime_formatter(date_style="long", time_style="short")
        formatted = formatter.format(dt)
        print(f"{name:15} {formatted}")


def demo_6_numeric_collation():
    """Demo 6: Smart numeric sorting."""
    print("\n=== Demo 6: Numeric vs Lexical Sorting ===")

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
    print("\nLexical sorting (incorrect for numbers):")
    for item in regular:
        print(f"  {item}")

    # Numeric sorting
    numeric = uicu.sort(items, "en-US", numeric=True)
    print("\nNumeric sorting (correct):")
    for item in numeric:
        print(f"  {item}")


def demo_7_text_transformation():
    """Demo 7: Unicode text transformations."""
    print("\n=== Demo 7: Text Transformations ===")

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

    print(f"Original: {original}")
    for transform_id, description in transforms:
        result = uicu.transliterate(original, transform_id)
        print(f"\n{description} ({transform_id}):")
        print(f"  {result}")
        if transform_id == "NFD":
            print(f"  Length: {len(original)} → {len(result)} characters")


def demo_8_script_detection():
    """Demo 8: Detect the primary script in text."""
    print("\n=== Demo 8: Script Detection ===")

    texts = [
        ("Hello, world!", "English"),
        ("Привет, мир!", "Russian"),
        ("你好世界", "Chinese"),
        ("مرحبا بالعالم", "Arabic"),
        ("Γεια σου κόσμε", "Greek"),
        ("שלום עולם", "Hebrew"),
        ("Mixed: Hello, 你好, مرحبا", "Mixed scripts"),
    ]

    for text, description in texts:
        script = uicu.detect_script(text)
        if script:
            script_name = uicu.script_name(script)
            print(f"{description:20} → {script} ({script_name})")
        else:
            print(f"{description:20} → Mixed/Unknown")


def demo_9_thai_word_breaking():
    """Demo 9: Word segmentation for languages without spaces."""
    print("\n=== Demo 9: Thai Word Segmentation ===")

    # Thai text without spaces between words
    thai_text = "สวัสดีครับยินดีต้อนรับสู่ประเทศไทย"
    print(f"Original Thai text: {thai_text}")
    print("(Thai doesn't use spaces between words)")

    # Segment into words
    words = list(uicu.words(thai_text, locale="th-TH"))
    # Filter out spaces
    words = [w for w in words if w.strip()]

    print(f"\nSegmented words ({len(words)}):")
    for i, word in enumerate(words, 1):
        print(f"  {i}. {word}")


def demo_10_emoji_handling():
    """Demo 10: Proper handling of emoji and complex graphemes."""
    print("\n=== Demo 10: Emoji and Complex Character Handling ===")

    # Text with various emoji
    text = "I ❤️ Python! 👨‍💻👩‍💻 Happy coding! 🇺🇸🇬🇧🇫🇷"

    print(f"Text: {text}")
    print(f"String length: {len(text)} (incorrect count)")

    # Count actual graphemes
    graphemes = list(uicu.graphemes(text))
    print(f"Grapheme count: {len(graphemes)} (correct count)")

    # Show complex graphemes
    complex_graphemes = [g for g in graphemes if len(g) > 1]
    print(f"\nComplex graphemes (multiple codepoints):")
    for g in complex_graphemes:
        codepoints = [f"U+{ord(c):04X}" for c in g]
        print(f"  '{g}' = {' + '.join(codepoints)}")


def demo_11_case_sensitive_sorting():
    """Demo 11: Control case sensitivity in sorting."""
    print("\n=== Demo 11: Case-Sensitive Sorting Control ===")

    words = ["Apple", "apple", "Banana", "banana", "Cherry", "cherry"]

    # Different collation strengths
    strengths = [
        ("primary", "Ignore case and accents"),
        ("secondary", "Consider accents, ignore case"),
        ("tertiary", "Consider case (default)"),
    ]

    for strength, description in strengths:
        collator = uicu.Collator("en-US", strength=strength)
        sorted_words = collator.sort(words)
        print(f"\n{description} (strength={strength}):")
        for word in sorted_words:
            print(f"  {word}")


def demo_12_bidirectional_text():
    """Demo 12: Handle mixed-direction text."""
    print("\n=== Demo 12: Bidirectional Text Handling ===")

    # Mixed LTR and RTL text
    examples = [
        "Hello שלום World",
        "The price is 123 ₪",
        "مرحبا Python مبرمج",
        "Email: user@example.com בעברית",
    ]

    print("Mixed-direction text examples:")
    for text in examples:
        print(f"\nText: {text}")

        # Analyze character directions
        def get_bidi_description(bidi_class):
            """Get human-readable description for bidirectional class."""
            if bidi_class in ["R", "AL"]:
                return "RTL"
            elif bidi_class == "L":
                return "LTR"
            elif bidi_class in ["EN", "AN"]:
                return "Number"
            else:
                return f"Other ({bidi_class})"

        for char in text:
            if char.strip():
                info = uicu.Char(char)
                bidi = info.bidirectional
                description = get_bidi_description(bidi)
                print(f"  '{char}' → {description}")


def main():
    """Run all demonstrations."""
    print("╔═══════════════════════════════════════════════════════╗")
    print("║          uicu - Unicode Text Processing Demos         ║")
    print("╚═══════════════════════════════════════════════════════╝")

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

    for i, demo in enumerate(demos, 1):
        print(f"\n{'=' * 60}")
        demo()
        # Non-interactive mode for scripting

    print("\n" + "=" * 60)
    print("All demos completed! Explore more at:")
    print("https://github.com/anthropics/uicu")


if __name__ == "__main__":
    main()
