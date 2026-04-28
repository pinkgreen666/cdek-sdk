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
from sdk.client import CdekClient


async def main():
    client = CdekClient(client_id="...", client_secret="...", test_mode=True)
    try:
        result = await client.location.get_location_suggest_cities("Москва", "RU")
        print(result)
    finally:
        await client.close()


asyncio.run(main())
```

