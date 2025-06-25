"""Test suite for uicu."""

import uicu


def test_version():
    """Verify package exposes version."""
    assert uicu.__version__
