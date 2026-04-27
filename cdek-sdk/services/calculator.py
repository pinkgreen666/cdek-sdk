from ..http.async_http import AsyncHTTPClient


class CalculatorService:
    def __init__(self, http_client: AsyncHTTPClient):
        self.__http = http_client

    async def post_calculator_tarifflist(self): ...

    async def post_calculator_tariff(self): ...

    async def post_calculator_tariffandservice(self): ...

    async def get_calculator_alltariffs(self): ...
