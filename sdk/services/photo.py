from ..http.async_http import AsyncHTTPClient


class PhotoService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_photodocument(self): ...

    async def get_photodocument_uuid(self): ...
