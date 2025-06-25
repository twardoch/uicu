#!/usr/bin/env python
# this_file: tests/test_segment.py
"""Tests for text segmentation module."""

import contextlib

import uicu


class TestGraphemeSegmentation:
    """Test grapheme cluster segmentation."""

    def test_basic_graphemes(self):
        """Test basic grapheme segmentation."""
        # Simple ASCII
        graphemes = list(uicu.graphemes("hello"))
        assert graphemes == ["h", "e", "l", "l", "o"]

        # With combining marks
        text = "café"  # e with acute accent
        graphemes = list(uicu.graphemes(text))
        assert len(graphemes) == 4  # c, a, f, é

    def test_emoji_graphemes(self):
        """Test emoji and complex grapheme clusters."""
        # Family emoji (multiple codepoints)
        family = "👨‍👩‍👧‍👦"
        graphemes = list(uicu.graphemes(family))
        assert len(graphemes) == 1  # Single grapheme cluster

        # Flag emoji
        flag = "🇺🇸"  # US flag
        graphemes = list(uicu.graphemes(flag))
        assert len(graphemes) == 1

        # Skin tone modifier
        wave = "👋🏽"  # Waving hand with skin tone
        graphemes = list(uicu.graphemes(wave))
        assert len(graphemes) == 1

    def test_grapheme_segmenter_class(self):
        """Test GraphemeSegmenter class."""
        segmenter = uicu.GraphemeSegmenter()

        # Test iteration
        text = "Hello 👋 World"
        graphemes = list(segmenter.segment(text))
        assert "H" in graphemes
        assert "👋" in graphemes

        # Test boundaries
        boundaries = segmenter.boundaries(text)
        assert 0 in boundaries  # Start
        assert len(text) in boundaries  # End


class TestWordSegmentation:
    """Test word boundary segmentation."""

    def test_basic_words(self):
        """Test basic word segmentation."""
        # English
        words = list(uicu.words("Hello, world!"))
        assert "Hello" in words
        assert "world" in words

        # Should not include punctuation as words
        assert "," not in words
        assert "!" not in words

    def test_contractions(self):
        """Test word segmentation with contractions."""
        # English contractions
        words = list(uicu.words("don't can't I'll"))
        # Behavior may vary by locale
        assert len(words) >= 3  # At least the three contracted forms

    def test_locale_specific_words(self):
        """Test locale-specific word segmentation."""
        # Thai (no spaces between words)
        thai_text = "สวัสดีครับ"
        words_th = list(uicu.words(thai_text, locale="th-TH"))
        assert len(words_th) > 0

        # Japanese
        japanese_text = "こんにちは世界"
        words_ja = list(uicu.words(japanese_text, locale="ja-JP"))
        assert len(words_ja) > 0

    def test_word_segmenter_class(self):
        """Test WordSegmenter class."""
        # Default locale with skip_whitespace
        segmenter = uicu.WordSegmenter(skip_whitespace=True)
        words = list(segmenter.segment("Hello world"))
        assert len(words) == 2
        assert words == ["Hello", "world"]

        # Specific locale
        segmenter_fr = uicu.WordSegmenter(locale="fr-FR", skip_whitespace=True)
        words_fr = list(segmenter_fr.segment("Bonjour le monde"))
        assert "Bonjour" in words_fr
        assert "monde" in words_fr

    def test_word_boundaries(self):
        """Test word boundary detection."""
        segmenter = uicu.WordSegmenter()
        text = "Hello world"
        boundaries = segmenter.boundaries(text)

        assert 0 in boundaries  # Start
        assert 5 in boundaries  # After "Hello"
        assert 6 in boundaries  # Start of "world"
        assert len(text) in boundaries  # End


class TestSentenceSegmentation:
    """Test sentence boundary segmentation."""

    def test_basic_sentences(self):
        """Test basic sentence segmentation."""
        text = "Hello world. How are you? I'm fine!"
        sentences = list(uicu.sentences(text))

        assert len(sentences) == 3
        assert "Hello world." in sentences[0]
        assert "How are you?" in sentences[1]
        assert "I'm fine!" in sentences[2]

    def test_abbreviations(self):
        """Test sentence segmentation with abbreviations."""
        text = "Dr. Smith went to Washington D.C. yesterday. He had a meeting."
        sentences = list(uicu.sentences(text))

        # ICU's sentence segmentation behavior can vary
        # Just check that we get reasonable sentences
        assert len(sentences) >= 2
        # Check the last sentence is recognized
        assert "He had a meeting." in sentences[-1]

    def test_multiple_punctuation(self):
        """Test sentences with multiple punctuation marks."""
        text = "Really?! That's amazing... Let me think."
        sentences = list(uicu.sentences(text))

        assert len(sentences) == 3
        assert "Really?!" in sentences[0]
        assert "amazing..." in sentences[1]

    def test_sentence_segmenter_class(self):
        """Test SentenceSegmenter class."""
        segmenter = uicu.SentenceSegmenter()

        text = "First sentence. Second sentence."
        sentences = list(segmenter.segment(text))
        assert len(sentences) == 2

        # Test boundaries
        boundaries = segmenter.boundaries(text)
        assert 0 in boundaries
        assert len(text) in boundaries


class TestLineBreaking:
    """Test line break segmentation."""

    def test_line_breaks(self):
        """Test finding line break opportunities."""
        text = "This is a very long line that might need to be broken."
        breaks = list(uicu.line_breaks(text))

        # Should find breaks at word boundaries
        assert len(breaks) > 5  # Multiple break opportunities

        # Should not break in middle of words
        word_starts = [i for i, c in enumerate(text) if i > 0 and text[i - 1] == " "]
        for start in word_starts:
            assert start in breaks or start + 1 in breaks


class TestSegmentationErrors:
    """Test error handling in segmentation."""

    def test_empty_text(self):
        """Test segmentation of empty text."""
        assert list(uicu.graphemes("")) == []
        assert list(uicu.words("")) == []
        assert list(uicu.sentences("")) == []

    def test_invalid_locale(self):
        """Test invalid locale handling."""
        # Should fall back to default or raise appropriate error
        with contextlib.suppress(uicu.OperationError):
            list(uicu.words("hello", locale="invalid_locale"))
