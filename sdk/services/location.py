from ..http.async_http import AsyncHTTPClient


class LocationService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_location_suggest_cities(
        self, name: str, country_code: str | None = None
    ):
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
        return result

    async def get_location_regions(
        self,
        country_codes: str | None = None,
        size: int | None = None,
        page: int | None = None,
        lang: str | None = None,
    ):
        """
        Метод предназначен для получения детальной информации о регионах.
        Список регионов может быть ограничен характеристиками, задаваемыми пользователем.

        Args:
            country_codes (str): Список кодов стран в формате ISO_3166-1_alpha-2
            size (int): Ограничение выборки результата. По умолчанию 1000. Обязателен, если указан page
            page (int): Номер страницы выборки результата. По умолчанию 0
            lang (str): Локализация. По умолчанию rus (доступны eng и zho)
        """
        params = {
            "country_codes": country_codes,
            "size": size,
            "page": page,
            "lang": lang,
        }

        result = await self._http.request("GET", "/v2/location/regions", params=params)
        return result

    async def get_location_postalcodes(self, city_code: int):
        """
        Метод предназначен для получения списка почтовых индексов.

        Args:
            city_code (int): Код города, которому принадлежат почтовые индексы
        """
        params = {"city_code": city_code}

        result = await self._http.request(
            "GET", "/v2/location/postalcodes", params=params
        )
        return result

    async def get_location_coordinates(self, latitude: float, longitude: float):
        """
        Метод позволяет определить локацию по переданным в запросе координатам

        Args:
            latitude (float): Широта
            longitude (float): Долгота
        """
        params = {"latitude": latitude, "longitude": longitude}

        result = await self._http.request(
            "GET", "/v2/location/cooridnates", params=params
        )
        return result

    async def get_location_cities(
        self,
        country_codes: str | None = None,
        region_code: int | None = None,
        kladr_region_code: str | None = None,
        kladr_code: str | None = None,
        flas_guid: str | None = None,
        postal_code: str | None = None,
        code: int | None = None,
        city: str | None = None,
        payment_limit: float | None = None,
        size: int | None = None,
        page: int | None = None,
        lang: str | None = None,
    ):
        """
        Метод предназначен для получения детальной информации о населенных пунктах.
        Список населенных пунктов может быть ограничен характеристиками, задаваемыми пользователем.

        Args:
            country_codes (str): Массив кодов стран в формате ISO_3166-1_alpha-2
            region_code (int): Код региона (справочник СДЭК)
            kladr_region_code (str): Код КЛАДР региона
            kladr_code (str): Код КЛАДР населенного пункта
            flas_guid (str): Уникальный идентификатор ФИАС населенного пункта
            postal_code (str): Почтовый индекс
            code (int): Код населенного пункта СДЭК
            city (str): Название населенного пункта. Должно соответствовать полностью
            payment_limit (float): Ограничение на сумму наложенного платежа. Особые значения: -1 - ограничения нет; 0 - наложенный платеж не принимается;
            size (int): Ограничение выборки результата. По умолчанию 1000. Обязателен, если указан page
            page (int): Номер страницы выборки результата. По умолчанию 0
            lang (str): Язык локализации ответа
        """
        params = {
            "country_codes": country_codes,
            "region_code": region_code,
            "kladr_region_code": kladr_region_code,
            "kladr_code": kladr_code,
            "flas_guid": flas_guid,
            "postal_code": postal_code,
            "code": code,
            "city": city,
            "payment_limit": payment_limit,
            "size": size,
            "page": page,
            "lang": lang,
        }

        result = await self._http.request("GET", "/v2/location/cities", params=params)
        return result
