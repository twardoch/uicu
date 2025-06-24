"""Test suite for uicu."""

def test_version():
    """Verify package exposes version."""
    import uicu
    assert uicu.__version__
