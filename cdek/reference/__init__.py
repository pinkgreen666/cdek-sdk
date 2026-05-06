"""Reference data for CDEK SDK."""

from cdek.reference.services import (
    get_service,
    list_services,
    get_packaging_services,
    suggest_box,
)
from cdek.reference.types import get_order_type, list_order_types
from cdek.reference.additional_types import get_additional_type, list_additional_types
from cdek.reference.delivery_modes import get_delivery_mode, list_delivery_modes

__all__ = [
    "get_service",
    "list_services",
    "get_packaging_services",
    "suggest_box",
    "get_order_type",
    "list_order_types",
    "get_additional_type",
    "list_additional_types",
    "get_delivery_mode",
    "list_delivery_modes",
]
