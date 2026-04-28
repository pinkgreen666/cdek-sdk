from typing import Any
import httpx


class AsyncHTTPClient:
    def __init__(
        self, client_id: str, client_secret: str, test_mode: bool, timeout: float = 30.0
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = (
            "https://api.edu.cdek.ru" if test_mode else "https://api.cdek.ru"
        )

        self._client = httpx.AsyncClient(timeout=timeout)
        self._access_token: str | None = None

    async def _auth(self) -> str | None:
        try:
            response = await self._client.post(
                f"{self.base_url}/v2/oauth/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            data = response.json()

            self._access_token = data["access_token"]

            return self._access_token

        except httpx.HTTPStatusError as e:
            detail = _response_detail(e.response)
            raise RuntimeError(
                f"CDEK auth failed with status {e.response.status_code}: {detail}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"CDEK auth failed: {e}") from e

    async def _ensure_token(self) -> str | None:
        if not self._access_token:
            return await self._auth()

        return self._access_token

    async def request(
        self, method: str, path: str, retry_auth: bool = True, **kwargs
    ) -> Any:
        params = kwargs.get("params")
        if isinstance(params, dict):
            kwargs["params"] = {
                key: value
                for key, value in params.items()
                if value is not None and value != ""
            }

        token = await self._ensure_token()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"

        try:
            response = await self._client.request(
                method=method, url=f"{self.base_url}{path}", headers=headers, **kwargs
            )

            if response.status_code == 401 and retry_auth:
                await self._auth()
                return await self.request(method, path, retry_auth=False, **kwargs)

            response.raise_for_status()

            if response.status_code == 204 or not response.content:
                return None

            return response.json()

        except httpx.HTTPStatusError as e:
            detail = _response_detail(e.response)
            raise RuntimeError(
                f"CDEK request failed with status {e.response.status_code}: {detail}"
            ) from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"CDEK request timed out: {e}") from e

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()


def _response_detail(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text
