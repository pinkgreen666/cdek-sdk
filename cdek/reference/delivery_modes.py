"""Delivery modes reference data."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from cdek.reference.models import DeliveryMode

_DATA_DIR = Path(__file__).parent / "data"


def _load_delivery_modes() -> Dict[int, DeliveryMode]:
    """Load delivery modes from JSON file."""
    with open(_DATA_DIR / "delivery_modes.json", encoding="utf-8") as f:
        data = json.load(f)
    return {item["code"]: DeliveryMode(**item) for item in data}


DELIVERY_MODES: Dict[int, DeliveryMode] = _load_delivery_modes()


def get_delivery_mode(code: int) -> Optional[DeliveryMode]:
    """Get delivery mode by code.

    Args:
        code: Delivery mode code

    Returns:
        DeliveryMode object or None if not found

    Example:
        >>> mode = get_delivery_mode(1)
        >>> print(mode.name)
        дверь-дверь
    """
    return DELIVERY_MODES.get(code)


def list_delivery_modes() -> List[DeliveryMode]:
    """List all delivery modes.

    Returns:
        List of DeliveryMode objects

    Example:
        >>> modes = list_delivery_modes()
        >>> for m in modes:
        ...     print(m.code, m.name)
    """
    return list(DELIVERY_MODES.values())
