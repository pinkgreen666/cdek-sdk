from ..http.async_http import AsyncHTTPClient


class DeliveryService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_delivery_intervals(self): ...

    async def post_delivery(self): ...

    async def get_delivery_uuid(self): ...

    async def post_delivery_estimaredintervals(self): ...
