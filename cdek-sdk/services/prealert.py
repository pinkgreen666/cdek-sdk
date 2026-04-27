from ..http.async_http import AsyncHTTPClient


class PrealertService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_prealert(self): ...

    async def get_prealert_uuid(self): ...
