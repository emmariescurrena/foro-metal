"""Test operations.py"""

from src.mates import operations as ops


def test_add():
    """Test add function"""
    assert ops.add(5) == 5


def test_substract():
    """Test substract function"""
    assert ops.substract(5) == -5


def test_multiply():
    """Test multiply function"""
    assert ops.multiply(4) == 4


def test_divide():
    """Test divide function"""
    assert ops.divide(4, 4) == 1
