"""Test verifications.py"""

from src.mates import verifications as ver


def test_is_odd():
    """Test is_odd function"""
    assert ver.is_odd(1) is True


def test_is_even():
    """Test is_even function"""
    assert ver.is_even(2) is True
