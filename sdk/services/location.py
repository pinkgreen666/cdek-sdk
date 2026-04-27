from ..http.async_http import AsyncHTTPClient


class LocationService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_location_suggest_cities(self, name: str, country_code: str | None):
        """
        Метод позволяет получать подсказки по подбору населенного пункта по его наименованию.
        Список населенных пунктов может быть ограничен характеристиками, задаваемыми пользователем.

        Args:
            name (str): Наименование населенного пункта СДЭК
            country_code (str | None): Код страны в формате ISO_3166-1_alpha-2

        """
        params = {"name": name, "country_code": country_code}

        result = await self._http.request(
            "GET", "/v2/location/suggest/cities", params=params
        )
        print(result)

    async def get_location_regions(self): ...

    async def get_location_postalcodes(self): ...

    async def get_location_coordinates(self): ...

    async def get_location_cities(self): ...
