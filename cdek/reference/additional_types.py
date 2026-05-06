"""Additional order types reference data."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from cdek.reference.models import OrderType

_DATA_DIR = Path(__file__).parent / "data"


def _load_additional_types() -> Dict[int, OrderType]:
    """Load additional order types from JSON file."""
    with open(_DATA_DIR / "additional_types.json", encoding="utf-8") as f:
        data = json.load(f)
    return {item["id"]: OrderType(**item) for item in data}


ADDITIONAL_TYPES: Dict[int, OrderType] = _load_additional_types()


def get_additional_type(type_id: int) -> Optional[OrderType]:
    """Get additional order type by ID.

    Args:
        type_id: Additional type ID

    Returns:
        OrderType object or None if not found

    Example:
        >>> add_type = get_additional_type(2)
        >>> print(add_type.name)
        для сборного груза (LTL)
    """
    return ADDITIONAL_TYPES.get(type_id)


def list_additional_types() -> List[OrderType]:
    """List all additional order types.

    Returns:
        List of OrderType objects

    Example:
        >>> types = list_additional_types()
        >>> for t in types:
        ...     print(t.id, t.name)
    """
    return list(ADDITIONAL_TYPES.values())
