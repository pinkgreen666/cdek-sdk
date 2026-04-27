from ..http.async_http import AsyncHTTPClient


class OfficeService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_deliverypoints(self): ...
