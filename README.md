# CDEK SDK

Async Python SDK for the CDEK API v2 (Russian logistics/delivery service).

## Features

- **Async/await support** - Built on `httpx` for high-performance async operations
- **Type safety** - Full Pydantic models for requests and responses
- **Automatic authentication** - OAuth2 token management with auto-retry on 401
- **Comprehensive error handling** - Custom exceptions for different error scenarios
- **Reference data** - Static data for services, packaging, order types, and delivery modes
- **Test mode** - Sandbox environment support for development

## Installation

### From wheel

Build:

```bash
python -m pip install -U build
python -m build --wheel
```

Install:

```bash
python -m pip install dist/*.whl
```

### From source

```bash
pip install -e .
```

## Quick Start

```python
import asyncio
from cdek import CdekClient


async def main():
    # Initialize client (test_mode=True for sandbox)
    client = CdekClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        test_mode=True
    )
    
    try:
        # Search for cities
        cities = await client.location.get_location_suggest_cities("Москва", "RU")
        print(f"Found {len(cities)} cities")
        
        # Calculate delivery cost
        tariff = await client.calculator.calculate_tariff(
            tariff_code=136,
            from_location={"code": 44},
            to_location={"code": 270},
            packages=[{"weight": 1000, "length": 10, "width": 10, "height": 10}]
        )
        print(f"Delivery cost: {tariff.delivery_sum} RUB")
        
    finally:
        await client.close()


asyncio.run(main())
```

### Using context manager

```python
async def main():
    async with CdekClient(client_id="...", client_secret="...", test_mode=True) as client:
        result = await client.location.get_location_suggest_cities("Москва", "RU")
        print(result)
```

## Available Services

The SDK provides access to all major CDEK API endpoints:

### Location Service
- `get_location_suggest_cities(city, country_codes)` - City search
- `get_location_suggest_postal_codes(postal_code, country_code)` - Postal code search
- `get_location_regions(country_codes, region_code, ...)` - Region listing
- `get_location_cities(country_codes, region_code, city, ...)` - City listing

### Office Service
- `get_deliverypoints(postal_code, city_code, type, ...)` - Delivery point search
- `get_deliverypoints_by_code(code)` - Get specific delivery point

### Calculator Service
- `calculate_tariff(tariff_code, from_location, to_location, packages, ...)` - Calculate delivery cost
- `calculate_tarifflist(from_location, to_location, packages, ...)` - Get all available tariffs

### Order Service
- `create_order(type, tariff_code, sender, recipient, packages, ...)` - Create delivery order
- `get_order(uuid)` - Get order by UUID
- `get_order_by_im_number(im_number)` - Get order by IM number
- `delete_order(uuid)` - Delete order
- `update_order(uuid, order_data)` - Update order

### Print Service
- `create_barcode(orders)` - Generate barcodes for orders
- `get_barcode(uuid)` - Get barcode by UUID
- `create_waybill(orders)` - Generate waybills
- `get_waybill(uuid)` - Get waybill by UUID

### Reference Service
- `get_additional_service_list()` - List additional services
- `get_tariff_list()` - List available tariffs
- `get_packaging_list()` - List packaging options

## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from cdek import CdekClient
from cdek.exceptions import (
    CdekError,
    CdekAuthError,
    CdekValidationError,
    CdekServerError,
    CdekTimeoutError,
)

async def main():
    async with CdekClient(client_id="...", client_secret="...", test_mode=True) as client:
        try:
            result = await client.calculator.calculate_tariff(
                tariff_code=136,
                from_location={"code": 44},
                to_location={"code": 270},
                packages=[{"weight": 1000, "length": 10, "width": 10, "height": 10}]
            )
            print(f"Delivery cost: {result.delivery_sum} RUB")
            
        except CdekAuthError as e:
            print(f"Authentication failed: {e.message}")
            
        except CdekValidationError as e:
            print(f"Invalid request: {e.message}")
            print(f"Details: {e.response_data}")
            
        except CdekServerError as e:
            print(f"Server error ({e.status_code}): {e.message}")
            
        except CdekTimeoutError as e:
            print(f"Request timed out: {e.message}")
            
        except CdekError as e:
            print(f"CDEK API error: {e.message}")
```

### Exception Hierarchy

- `CdekError` - Base exception (catch all CDEK errors)
  - `CdekAuthError` - Authentication failures (401)
  - `CdekValidationError` - Request validation errors (400)
  - `CdekNotFoundError` - Resource not found (404)
  - `CdekServerError` - Server errors (500, 502, 503, 504)
  - `CdekRateLimitError` - Rate limit exceeded (429)
  - `CdekTimeoutError` - Request timeout
  - `CdekNetworkError` - Network connection errors

All exceptions include:
- `message` - Error description
- `status_code` - HTTP status code (if applicable)
- `response_data` - Raw response data from the API

## Reference Data

The SDK includes static reference data from CDEK documentation for information that doesn't have API endpoints.

```python
from cdek.reference import (
    get_service, list_services, suggest_box, get_packaging_services,
    get_order_type, list_order_types,
    get_additional_type, list_additional_types,
    get_delivery_mode, list_delivery_modes
)

# Get service information
service = get_service("INSURANCE")
print(f"{service.name}: {service.description}")

# Get packaging recommendation
box = suggest_box(weight=3.5, mode="warehouse-door")
print(f"Recommended: {box.name} ({box.dimensions} cm, max {box.max_weight} kg)")

# List services for specific delivery mode
services = list_services(mode="warehouse-door", max_weight=10.0)

# Get all packaging options
packages = get_packaging_services()
for pkg in packages:
    print(f"{pkg.code}: {pkg.name} - {pkg.dimensions} cm")

# Get order type
order_type = get_order_type(1)
print(order_type.name)  # интернет-магазин

# Get delivery mode
mode = get_delivery_mode(1)
print(f"Mode {mode.code}: {mode.name}")  # Mode 1: дверь-дверь

# List all delivery modes
modes = list_delivery_modes()
for m in modes:
    print(f"{m.code}: {m.name}")
```

### Available Reference Data

- **Additional services** - Insurance, notifications, try-on, packaging, special handling
- **Packaging options** - Boxes and envelopes with dimensions and weight limits
- **Order types** - Main order types (интернет-магазин, доставка)
- **Additional order types** - Special types (LTL, Forward, Fulfillment, etc.)
- **Delivery modes** - All delivery modes (дверь-дверь, склад-склад, постамат-постамат, etc.)

### Common Service Codes

**Delivery services:**
- `INSURANCE` - Package insurance
- `TAKE_SENDER` - Pickup from sender
- `DELIV_RECEIVER` - Delivery to receiver
- `TRYING_ON` - Try-on service (e-commerce)
- `PART_DELIV` - Partial delivery (e-commerce)

**Notifications:**
- `SMS` - SMS notification to sender
- `NOTIFY_ORDER_CREATED` - SMS to recipient on order creation
- `NOTIFY_ORDER_DELIVERY` - SMS to recipient on delivery
- `SMS_NOTIFICATIONS_FOR_THE_RECIPIENT` - SMS on arrival

**Packaging:**
- `CARTON_BOX_XS` - 0.5 kg, 17×12×9 cm
- `CARTON_BOX_S_2_KILOS` - 2 kg, 23×19×10 cm
- `CARTON_BOX_M` - 5 kg, 33×25×15 cm
- `CARTON_BOX_10KG` - 10 kg, 40×35×28 cm
- `CARTON_BOX_20KG` - 20 kg, 47×40×43 cm
- `CARTON_BOX_30KG` - 30 kg, 69×39×42 cm

See `cdek/reference/README.md` for detailed documentation.

## Testing

The SDK includes a comprehensive test suite using pytest.

### Setup

Install test dependencies:

```bash
pip install pytest pytest-asyncio
```

Set environment variables for live API tests:

```bash
export CDEK_CLIENT_ID="your_client_id"
export CDEK_CLIENT_SECRET="your_client_secret"
export CDEK_TEST_MODE="true"  # Use sandbox API
```

### Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_calculator.py
```

Run with verbose output:

```bash
pytest -v -s
```

Run only unit tests (no API calls):

```bash
pytest tests/test_async_http.py tests/test_reference.py
```

### Test Structure

- `tests/test_async_http.py` - HTTP client unit tests
- `tests/test_calculator.py` - Calculator service tests
- `tests/test_location.py` - Location service tests
- `tests/test_office.py` - Office service tests
- `tests/test_order.py` - Order service tests
- `tests/test_print.py` - Print service tests
- `tests/test_reference.py` - Reference data tests
- `tests/conftest.py` - Shared fixtures and configuration

Tests that require API credentials are automatically skipped if credentials are not provided.

## Development

### Project Structure

```
cdek-sdk/
├── cdek/
│   ├── __init__.py
│   ├── client.py              # Main CdekClient
│   ├── exceptions.py          # Custom exceptions
│   ├── http/
│   │   └── async_http.py      # HTTP client with OAuth2
│   ├── models/                # Pydantic models
│   │   ├── calculator.py
│   │   ├── location.py
│   │   ├── office.py
│   │   ├── order.py
│   │   ├── print.py
│   │   └── reference.py
│   ├── services/              # API service classes
│   │   ├── calculator.py
│   │   ├── location.py
│   │   ├── office.py
│   │   ├── order.py
│   │   ├── print.py
│   │   └── reference.py
│   └── reference/             # Static reference data
│       ├── models/
│       ├── data/
│       └── *.py
├── tests/
├── CLAUDE.md                  # Development guidelines
└── README.md
```

### Building

Build wheel package:

```bash
python -m pip install -U build
python -m build --wheel
```

Install in development mode:

```bash
pip install -e .
```

## Environment Modes

The SDK supports two environments:

- **Test mode** (`test_mode=True`) - Sandbox API at `https://api.edu.cdek.ru`
- **Production mode** (`test_mode=False`) - Production API at `https://api.cdek.ru`

Always use test mode during development and testing.

## Authentication

The SDK handles OAuth2 authentication automatically:

1. On first request, fetches access token using client credentials
2. Stores token and reuses it for subsequent requests
3. Automatically retries with new token if 401 is received
4. No manual token management required

## Dependencies

- `httpx` - Async HTTP client
- `pydantic` (v1.10.18) - Data validation and models
- `pytest` + `pytest-asyncio` - Testing framework (dev)

## License

MIT

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass (`pytest`)
2. Code follows existing patterns
3. New features include tests
4. Documentation is updated

## Support

For issues and questions, please open an issue on the project repository.
