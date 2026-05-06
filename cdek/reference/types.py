"""Order types reference data."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from cdek.reference.models import OrderType

_DATA_DIR = Path(__file__).parent / "data"


def _load_order_types() -> Dict[int, OrderType]:
    """Load order types from JSON file."""
    with open(_DATA_DIR / "types.json", encoding="utf-8") as f:
        data = json.load(f)
    return {item["id"]: OrderType(**item) for item in data}


ORDER_TYPES: Dict[int, OrderType] = _load_order_types()


def get_order_type(type_id: int) -> Optional[OrderType]:
    """Get order type by ID.

    Args:
        type_id: Order type ID

    Returns:
        OrderType object or None if not found

    Example:
        >>> order_type = get_order_type(1)
        >>> print(order_type.name)
        интернет-магазин
    """
    return ORDER_TYPES.get(type_id)


def list_order_types() -> List[OrderType]:
    """List all order types.

    Returns:
        List of OrderType objects

    Example:
        >>> types = list_order_types()
        >>> for t in types:
        ...     print(t.id, t.name)
    """
    return list(ORDER_TYPES.values())
