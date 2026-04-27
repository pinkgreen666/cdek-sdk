from ..http.async_http import AsyncHTTPClient


class WebhooksService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_webhooks(self): ...

    async def post_webhooks(self): ...

    async def get_webhooks_uuid(self): ...

    async def delete_webhooks_uuid(self): ...
