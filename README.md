# cdek_api_sdk

Async Python SDK for the CDEK API v2.

## Install (wheel)

Build:

```bash
python -m pip install -U build
python -m build --wheel
```

Install:

```bash
python -m pip install dist/*.whl
```

## Quick start

```python
import asyncio
from cdek import CdekClient


async def main():
    client = CdekClient(client_id="...", client_secret="...", test_mode=True)
    try:
        result = await client.location.get_location_suggest_cities("Москва", "RU")
        print(result)
    finally:
        await client.close()


asyncio.run(main())
```

## Error Handling

The SDK provides custom exceptions to handle different error scenarios gracefully:

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
    client = CdekClient(client_id="...", client_secret="...", test_mode=True)
    
    try:
        result = await client.calculator.calculate_tariff(
            tariff_code=1,
            from_location={"code": 44},
            to_location={"code": 270},
            packages=[{"weight": 1000, "length": 10, "width": 10, "height": 10}]
        )
        print(f"Delivery cost: {result}")
        
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
        
    finally:
        await client.close()
```

### Available Exceptions

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

See `examples/error_handling.py` for more patterns including retry logic and graceful degradation.

