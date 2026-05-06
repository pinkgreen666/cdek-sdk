"""Services reference data."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from cdek.reference.models import Service

_DATA_DIR = Path(__file__).parent / "data"


def _load_services() -> Dict[str, Service]:
    """Load services from JSON file."""
    with open(_DATA_DIR / "services.json", encoding="utf-8") as f:
        data = json.load(f)
    return {item["code"]: Service(**item) for item in data}


SERVICES: Dict[str, Service] = _load_services()


def get_service(code: str) -> Optional[Service]:
    """Get service by code.

    Args:
        code: Service code (e.g., "INSURANCE", "TRYING_ON")

    Returns:
        Service object or None if not found

    Example:
        >>> service = get_service("INSURANCE")
        >>> print(service.name)
        Страхование
    """
    return SERVICES.get(code)


def list_services(
    mode: Optional[str] = None, max_weight: Optional[float] = None
) -> List[Service]:
    """List all services with optional filters.

    Args:
        mode: Filter by delivery mode (e.g., "warehouse-door")
        max_weight: Filter services available for this weight

    Returns:
        List of Service objects

    Example:
        >>> services = list_services(mode="warehouse-door")
        >>> for s in services:
        ...     print(s.code, s.name)
    """
    services = list(SERVICES.values())

    if mode:
        services = [s for s in services if s.modes is None or mode in s.modes]

    if max_weight is not None:
        services = [
            s
            for s in services
            if s.weight_limit is None or s.weight_limit >= max_weight
        ]

    return services


def get_packaging_services() -> List[Service]:
    """Get all packaging-related services (boxes, envelopes, etc.).

    Returns:
        List of packaging services
    """
    packaging_codes = [
        "CARTON_BOX_XS",
        "CARTON_BOX_S_2_KILOS",
        "CARTON_BOX_M",
        "CARTON_BOX_2KG",
        "CARTON_BOX_3KG",
        "CARTON_BOX_5KG",
        "CARTON_BOX_10KG",
        "CARTON_BOX_L_12_KILOS",
        "CARTON_BOX_XL_18_KILOS",
        "CARTON_BOX_20KG",
        "CARTON_BOX_30KG",
        "COURIER_PACKAGE_A2",
        "PACKAGE_A_2_LIGHT_EXPRESS",
        "PACKAGE_A_3_LIGHT_EXPRESS",
        "PACKAGE_A_4_LIGHT_EXPRESS",
        "PACKAGE_A_5_LIGHT_EXPRESS",
        "ENVELOPE_A4_CDEK_FREE",
    ]
    return [SERVICES[code] for code in packaging_codes if code in SERVICES]


def suggest_box(
    weight: float, mode: str = "warehouse-door"
) -> Optional[Service]:
    """Suggest appropriate box based on weight and delivery mode.

    Args:
        weight: Package weight in kg
        mode: Delivery mode

    Returns:
        Recommended box service or None

    Example:
        >>> box = suggest_box(3.5, "warehouse-door")
        >>> print(box.name)
        Коробка (5 кг 40х24х21 см)
    """
    boxes = [
        s
        for s in get_packaging_services()
        if s.code.startswith("CARTON_BOX_")
        and s.max_weight is not None
        and s.max_weight >= weight
        and (s.modes is None or mode in s.modes)
    ]

    if not boxes:
        return None

    return min(boxes, key=lambda b: b.max_weight)
