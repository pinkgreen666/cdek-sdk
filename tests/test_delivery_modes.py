"""Tests for delivery modes reference data."""

import pytest
from cdek.reference import get_delivery_mode, list_delivery_modes


def test_get_delivery_mode():
    """Test getting delivery mode by code."""
    mode = get_delivery_mode(1)
    assert mode is not None
    assert mode.code == 1
    assert mode.name == "дверь-дверь"


def test_get_delivery_mode_not_found():
    """Test getting non-existent delivery mode."""
    mode = get_delivery_mode(999)
    assert mode is None


def test_list_delivery_modes():
    """Test listing all delivery modes."""
    modes = list_delivery_modes()
    assert len(modes) == 9
    codes = [m.code for m in modes]
    assert 1 in codes
    assert 2 in codes
    assert 10 in codes
    assert 5 not in codes  # Code 5 doesn't exist


def test_delivery_mode_names():
    """Test specific delivery mode names."""
    test_cases = {
        1: "дверь-дверь",
        2: "дверь-склад",
        3: "склад-дверь",
        4: "склад-склад",
        6: "дверь-постамат",
        7: "склад-постамат",
        8: "постамат-дверь",
        9: "постамат-склад",
        10: "постамат-постамат",
    }

    for code, expected_name in test_cases.items():
        mode = get_delivery_mode(code)
        assert mode is not None
        assert mode.name == expected_name
