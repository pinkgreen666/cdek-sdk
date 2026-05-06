# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an async Python SDK for the CDEK API v2 (Russian logistics/delivery service). The SDK provides a clean interface to interact with CDEK's REST API, handling authentication, request management, and response parsing.

## Architecture

**Client Structure**: The SDK uses a service-oriented architecture where `CdekClient` acts as the main entry point and delegates to specialized service classes:

- `CdekClient` (cdek/client.py) - Main client that initializes all services and manages the HTTP client lifecycle
- `AsyncHTTPClient` (cdek/http/async_http.py) - Handles OAuth2 authentication, token management, and HTTP requests with automatic retry on 401
- Service classes (cdek/services/*.py) - Each service wraps a specific API domain (location, office, calculator, order, etc.)

**Authentication Flow**: The HTTP client automatically handles OAuth2 client credentials flow. It fetches an access token on first request and retries authentication if a 401 is received. Tokens are stored in `_access_token` and reused across requests.

**Environment Modes**: The SDK supports two modes via `test_mode` parameter:
- `test_mode=True` → `https://api.edu.cdek.ru` (sandbox)
- `test_mode=False` → `https://api.cdek.ru` (production)

**Models**: Pydantic models (cdek/models/) define request/response schemas for all services:
- `calculator.py` - Request DTOs and response models for calculator service
- `location.py` - Response models for location service
- `office.py` - Response models for office/deliverypoints service
- `reference.py` - Models for reference data (additional services, tariffs, packaging)

All service methods return typed Pydantic models for better IDE support and validation.

**Reference Data**: The SDK includes static reference data from CDEK documentation that doesn't have API endpoints:
- `cdek/reference/` - Reference data module with helper functions
- `cdek/reference/data/additional_services.json` - All additional services (insurance, packaging, notifications, etc.)
- Access via `from cdek.reference import get_service, list_services, suggest_box`

## Development Commands

**Build the package**:
```bash
python -m pip install -U build
python -m build --wheel
```

**Install locally**:
```bash
python -m pip install dist/*.whl
```

**Run tests**:
```bash
pytest
```

**Run specific test file**:
```bash
pytest tests/test_calculator.py
```

**Run tests with output**:
```bash
pytest -v -s
```

## Testing

Tests use pytest with pytest-asyncio for async test support. The test suite includes:

- Live API tests that require credentials (tests/conftest.py provides fixtures)
- Unit tests for HTTP client behavior (tests/test_async_http.py)
- Service-level integration tests (tests/test_calculator.py, tests/test_location.py, etc.)

**Environment variables for live tests**:
- `CDEK_CLIENT_ID` - CDEK API client ID (required)
- `CDEK_CLIENT_SECRET` - CDEK API client secret (required)
- `CDEK_TEST_MODE` - Set to "1", "true", "yes", or "on" to use sandbox API (default: true)

Tests are skipped if credentials are not provided. The `live_client` fixture in conftest.py handles client setup and teardown.

## Code Patterns

**Service methods**: All service methods are async and follow this pattern:
1. Accept typed parameters (use Pydantic models for complex objects)
2. Build params dict, filtering out None/empty values (handled by AsyncHTTPClient)
3. Call `self._http.request(method, path, params=params)` or with `json=body`
4. Parse response into Pydantic model and return it

All service methods return typed Pydantic models (or lists of models) for type safety and IDE support.

**Error handling**: The SDK provides custom exceptions for different error scenarios. All exceptions inherit from `CdekError` and include `message`, `status_code`, and `response_data` attributes. See the "Error Handling" section below for details.

**Client lifecycle**: Always close the client after use:
```python
client = CdekClient(...)
try:
    result = await client.location.get_location_suggest_cities("Москва", "RU")
finally:
    await client.close()
```

Or use as async context manager:
```python
async with CdekClient(...) as client:
    result = await client.location.get_location_suggest_cities("Москва", "RU")
```

## Error Handling

The SDK provides custom exceptions for different error scenarios. All exceptions inherit from `CdekError` base class.

**Exception hierarchy**:
- `CdekError` - Base exception with `message`, `status_code`, and `response_data` attributes
  - `CdekAuthError` - Authentication failures (401, invalid credentials)
  - `CdekValidationError` - Request validation errors (400)
  - `CdekNotFoundError` - Resource not found (404)
  - `CdekServerError` - Server errors (500, 502, 503, 504)
  - `CdekRateLimitError` - Rate limit exceeded (429)
  - `CdekTimeoutError` - Request timeout
  - `CdekNetworkError` - Network connection errors

**Usage pattern**:
```python
from cdek import CdekClient
from cdek.exceptions import CdekError, CdekServerError

client = CdekClient(...)
try:
    result = await client.calculator.calculate_tariff(...)
except CdekServerError as e:
    # Handle server errors specifically
    print(f"Server error: {e.message}, status: {e.status_code}")
except CdekError as e:
    # Catch all other CDEK errors
    print(f"API error: {e.message}")
finally:
    await client.close()
```

See `examples/error_handling.py` for comprehensive error handling patterns including retry logic and graceful degradation.

## Error Handling

The SDK provides custom exceptions for different error scenarios. All exceptions inherit from `CdekError` base class.

**Exception hierarchy**:
- `CdekError` - Base exception with `message`, `status_code`, and `response_data` attributes
  - `CdekAuthError` - Authentication failures (401, invalid credentials)
  - `CdekValidationError` - Request validation errors (400)
  - `CdekNotFoundError` - Resource not found (404)
  - `CdekServerError` - Server errors (500, 502, 503, 504)
  - `CdekRateLimitError` - Rate limit exceeded (429)
  - `CdekTimeoutError` - Request timeout
  - `CdekNetworkError` - Network connection errors

**Usage pattern**:
```python
from cdek import CdekClient
from cdek.exceptions import CdekError, CdekServerError

client = CdekClient(...)
try:
    result = await client.calculator.calculate_tariff(...)
except CdekServerError as e:
    # Handle server errors specifically
    print(f"Server error: {e.message}, status: {e.status_code}")
except CdekError as e:
    # Catch all other CDEK errors
    print(f"API error: {e.message}")
finally:
    await client.close()
```

See `examples/error_handling.py` for comprehensive error handling patterns including retry logic and graceful degradation.

## Reference Data

The SDK includes static reference data from CDEK documentation for information that doesn't have API endpoints.

**Module structure**:
- `cdek/reference/models/` - Pydantic models (Service, OrderType, DeliveryMode)
- `cdek/reference/services.py` - Additional services functions
- `cdek/reference/types.py` - Order types functions
- `cdek/reference/additional_types.py` - Additional order types functions
- `cdek/reference/delivery_modes.py` - Delivery modes functions
- `cdek/reference/data/` - JSON data files

**Available reference data**:
- Services (insurance, packaging, notifications, delivery options, etc.)
- Order types (интернет-магазин, доставка)
- Additional types (LTL, Forward, Fulfillment, etc.)
- Delivery modes (дверь-дверь, склад-склад, постамат-постамат, etc.)

**Usage examples**:
```python
from cdek.reference import (
    get_service, list_services, suggest_box, get_packaging_services,
    get_order_type, list_order_types,
    get_additional_type, list_additional_types,
    get_delivery_mode, list_delivery_modes
)

# Get service details
service = get_service("INSURANCE")
print(service.name, service.description)

# List services with filters
services = list_services(mode="warehouse-door", max_weight=10.0)

# Get packaging recommendations
box = suggest_box(weight=3.5, mode="warehouse-door")
print(f"Recommended: {box.name}, max {box.max_weight}kg")

# Get all packaging options
packages = get_packaging_services()

# Get order type
order_type = get_order_type(1)
print(order_type.name)  # интернет-магазин

# Get additional type
add_type = get_additional_type(2)
print(add_type.name)  # для сборного груза (LTL)

# Get delivery mode
mode = get_delivery_mode(1)
print(mode.name)  # дверь-дверь

# List all delivery modes
modes = list_delivery_modes()
for m in modes:
    print(f"{m.code}: {m.name}")
```

**Integration with FastAPI**:
See `examples/fastapi_reference.py` for a complete FastAPI backend that uses reference data to build delivery configuration APIs. The example includes:
- Service listing and filtering endpoints
- Packaging suggestion endpoint
- Delivery wizard that combines API calls with reference data
- Frontend-ready response formats

**Frontend integration**:
See `examples/react_delivery_selector.tsx` for React components that consume the FastAPI endpoints to build:
- Service selection UI with restrictions display
- Packaging selector with recommendations
- Complete delivery configuration wizard

## Dependencies

- `httpx` - Async HTTP client
- `pydantic` (v1.10.18) - Data validation and models
- `pytest` + `pytest-asyncio` - Testing framework
