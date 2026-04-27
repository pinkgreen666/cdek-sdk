from ..http.async_http import AsyncHTTPClient


class InternationalService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_international_package_restriction(self): ...
