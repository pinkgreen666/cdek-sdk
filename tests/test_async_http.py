import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch
from sdk.http.async_http import AsyncHTTPClient


@pytest.mark.asyncio
async def test_async_http_client_auth():
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.post = AsyncMock()
        mock_client.post.return_value = MagicMock(spec=httpx.Response)
        mock_client.post.return_value.status_code = 200
        mock_client.post.return_value.json.return_value = {"access_token": "fake_token"}

        client = AsyncHTTPClient("id", "secret", test_mode=True)
        token = await client._auth()
        print(token)

        assert token == "fake_token"
        assert client._access_token == "fake_token"
        mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_async_http_client_request():
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = mock_client_class.return_value

        # Mock auth
        mock_client.post = AsyncMock()
        mock_client.post.return_value = MagicMock(spec=httpx.Response)
        mock_client.post.return_value.status_code = 200
        mock_client.post.return_value.json.return_value = {"access_token": "fake_token"}

        # Mock request
        mock_client.request = AsyncMock()
        mock_client.request.return_value = MagicMock(spec=httpx.Response)
        mock_client.request.return_value.status_code = 200
        mock_client.request.return_value.json.return_value = {"data": "ok"}
        mock_client.request.return_value.content = b'{"data": "ok"}'

        client = AsyncHTTPClient("id", "secret", test_mode=True)
        result = await client.request("GET", "/test")

        assert result == {"data": "ok"}
        mock_client.request.assert_called_once()
        # Verify Authorization header
        args, kwargs = mock_client.request.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer fake_token"
