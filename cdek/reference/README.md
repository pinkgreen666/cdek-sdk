# CDEK Reference Data

This module contains static reference data from CDEK documentation that doesn't have API endpoints.

## Module Structure

```
cdek/reference/
├── models/              # Pydantic models
│   ├── service.py      # Service model
│   └── order_type.py   # OrderType model
├── services.py         # Services functions
├── types.py            # Order types functions
├── additional_types.py # Additional types functions
└── data/               # JSON data files
    ├── services.json
    ├── types.json
    └── additional_types.json
```

## What's included

- **Services** - All CDEK additional services with descriptions, restrictions, and requirements
- **Order types** - Main order types (интернет-магазин, доставка)
- **Additional types** - Special order types (LTL, Forward, Fulfillment, etc.)
- **Packaging options** - Boxes, envelopes, and packaging materials with dimensions and weight limits

## Usage

### Services

```python
from cdek.reference import get_service, list_services

# Get specific service
service = get_service("INSURANCE")
print(service.name)  # "Страхование"
print(service.description)
print(service.auto_added)  # True - added automatically for e-commerce

# List all services
all_services = list_services()

# Filter by delivery mode
warehouse_services = list_services(mode="warehouse-door")

# Filter by weight
light_services = list_services(max_weight=5.0)
```

### Order types

```python
from cdek.reference import get_order_type, list_order_types

# Get order type by ID
order_type = get_order_type(1)
print(order_type.name)  # "интернет-магазин"

# List all order types
types = list_order_types()
```

### Additional types

```python
from cdek.reference import get_additional_type, list_additional_types

# Get additional type by ID
add_type = get_additional_type(2)
print(add_type.name)  # "для сборного груза (LTL)"

# List all additional types
types = list_additional_types()
```

### Packaging suggestions

```python
from cdek.reference import suggest_box, get_packaging_services

# Get recommended box for weight and mode
box = suggest_box(weight=3.5, mode="warehouse-door")
print(f"{box.name} - {box.dimensions} cm, max {box.max_weight} kg")

# Get all packaging options
packages = get_packaging_services()
for pkg in packages:
    print(f"{pkg.code}: {pkg.name}")
```

### Service validation

```python
from cdek.reference import get_service

# Check service restrictions before using
service = get_service("TRYING_ON")
if service.restrictions:
    print(f"⚠️ {service.restrictions}")

# Check if service requires parameters
floor_service = get_service("GET_UP_FLOOR_BY_HAND")
if floor_service.requires_parameter:
    print("This service needs a parameter (number of floors)")
```

## Integration examples

### FastAPI backend

See `examples/fastapi_reference.py` for a complete FastAPI application that provides:

- `/api/services` - List services with filters
- `/api/services/{code}` - Get service details
- `/api/packaging` - List packaging options
- `/api/packaging/suggest` - Get packaging recommendation
- `/api/delivery-wizard` - Complete delivery configuration helper

### React frontend

See `examples/react_delivery_selector.tsx` for React components:

- `DeliveryServiceSelector` - Complete delivery configuration UI
- `ServiceDetailsModal` - Service information modal
- `PackagingSelector` - Packaging selection with recommendations

## Data structure

### Service model

```python
class Service(BaseModel):
    code: str                           # Service code (e.g., "INSURANCE")
    name: str                           # Display name
    description: str                    # Full description
    modes: Optional[List[str]]          # Allowed delivery modes
    weight_limit: Optional[float]       # Weight limit in kg
    max_weight: Optional[float]         # Max weight for packaging
    dimensions: Optional[str]           # Dimensions for packaging
    requires_parameter: bool            # Whether service needs parameter
    auto_added: bool                    # Added automatically by CDEK
    restrictions: Optional[str]         # Usage restrictions
```

### OrderType model

```python
class OrderType(BaseModel):
    id: int                             # Type ID
    name: str                           # Display name
```

## Common service codes

### Delivery services
- `INSURANCE` - Package insurance
- `TAKE_SENDER` - Pickup from sender
- `DELIV_RECEIVER` - Delivery to receiver
- `TRYING_ON` - Try-on service (e-commerce)
- `PART_DELIV` - Partial delivery (e-commerce)

### Notifications
- `SMS` - SMS notification to sender
- `NOTIFY_ORDER_CREATED` - SMS to recipient on order creation
- `NOTIFY_ORDER_DELIVERY` - SMS to recipient on delivery
- `SMS_NOTIFICATIONS_FOR_THE_RECIPIENT` - SMS on arrival
- `SMS_NOTIFICATIONS_FOR_EXPIRATION_DATE` - SMS on storage expiration

### Packaging
- `CARTON_BOX_XS` - 0.5 kg, 17×12×9 cm
- `CARTON_BOX_S_2_KILOS` - 2 kg, 23×19×10 cm
- `CARTON_BOX_M` - 5 kg, 33×25×15 cm
- `CARTON_BOX_10KG` - 10 kg, 40×35×28 cm
- `CARTON_BOX_20KG` - 20 kg, 47×40×43 cm
- `CARTON_BOX_30KG` - 30 kg, 69×39×42 cm

### Special services
- `GET_UP_FLOOR_BY_HAND` - Carry up stairs (requires floor count parameter)
- `GET_UP_FLOOR_BY_ELEVATOR` - Elevator delivery
- `ADULT_GOODS` - Age verification (18+)
- `BAN_ATTACHMENT_INSPECTION` - Prohibit package inspection
- `PHOTO_OF_DOCUMENTS` - Photo documentation

## Adding new reference data

To add more reference data:

1. Create JSON file in `cdek/reference/data/`
2. Define Pydantic model in `cdek/reference/models/`
3. Create module file in `cdek/reference/` (e.g., `tariffs.py`)
4. Export functions in `cdek/reference/__init__.py`
5. Add tests in `tests/test_reference.py`

Example:

```python
# cdek/reference/models/tariff.py
from pydantic import BaseModel

class Tariff(BaseModel):
    code: int
    name: str
    mode: str

# cdek/reference/tariffs.py
import json
from pathlib import Path
from typing import Dict, Optional
from cdek.reference.models import Tariff

_DATA_DIR = Path(__file__).parent / "data"

def _load_tariffs() -> Dict[int, Tariff]:
    with open(_DATA_DIR / "tariffs.json", encoding="utf-8") as f:
        data = json.load(f)
    return {item["code"]: Tariff(**item) for item in data}

TARIFFS: Dict[int, Tariff] = _load_tariffs()

def get_tariff(code: int) -> Optional[Tariff]:
    return TARIFFS.get(code)

# cdek/reference/__init__.py
from cdek.reference.tariffs import get_tariff

__all__ = [..., "get_tariff"]
```

## Testing

Run reference data tests:

```bash
pytest tests/test_reference.py -v
```

All reference data is validated against Pydantic models to ensure type safety.
