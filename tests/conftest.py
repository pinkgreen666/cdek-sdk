import json
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from cdek.client import CdekClient

# Load environment variables from .env file
load_dotenv()


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    pytest.skip(f"Set the {name} environment variable to run live CDEK API tests.")


def _print_cdek_response(label: str, payload) -> None:
    print(f"\n=== {label} ===")
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


@pytest_asyncio.fixture
async def live_client():
    client = CdekClient(
        client_id=_require_env("CDEK_CLIENT_ID"),
        client_secret=_require_env("CDEK_CLIENT_SECRET"),
        test_mode=_env_flag("CDEK_TEST_MODE", True),
    )
    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
def cdek_response_printer():
    return _print_cdek_response
