"""Test error handling."""

import pytest
from cdek import CdekClient
from cdek.exceptions import (
    CdekError,
    CdekAuthError,
    CdekValidationError,
    CdekNotFoundError,
    CdekServerError,
    CdekTimeoutError,
    CdekNetworkError,
)


@pytest.mark.asyncio
async def test_invalid_credentials():
    """Test that invalid credentials raise CdekAuthError."""
    client = CdekClient(
        client_id="invalid",
        client_secret="invalid",
        test_mode=True
    )

    try:
        with pytest.raises(CdekAuthError) as exc_info:
            await client.location.get_location_suggest_cities("Moscow", "RU")

        assert exc_info.value.status_code == 401
        assert exc_info.value.response_data is not None
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_error_attributes():
    """Test that errors have proper attributes."""
    client = CdekClient(
        client_id="invalid",
        client_secret="invalid",
        test_mode=True
    )

    try:
        await client.location.get_location_suggest_cities("Moscow", "RU")
    except CdekError as e:
        assert hasattr(e, "message")
        assert hasattr(e, "status_code")
        assert hasattr(e, "response_data")
        assert e.status_code is not None
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_catch_base_exception():
    """Test that all errors can be caught with base CdekError."""
    client = CdekClient(
        client_id="invalid",
        client_secret="invalid",
        test_mode=True
    )

    try:
        with pytest.raises(CdekError):
            await client.location.get_location_suggest_cities("Moscow", "RU")
    finally:
        await client.close()
