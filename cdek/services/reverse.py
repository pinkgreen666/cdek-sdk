from ..http.async_http import AsyncHTTPClient


class ReverseService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_reverse_availability(self): ...
