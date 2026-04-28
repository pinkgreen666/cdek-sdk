from ..http.async_http import AsyncHTTPClient


class OfficeService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_deliverypoints(
        self,
        code: str | None = None,
        type: str | None = None,
        postal_code: str | None = None,
        city_code: int | None = None,
        country_code: str | None = None,
        region_code: int | None = None,
        have_cashless: bool | None = None,
        have_cash: bool | None = None,
        allowed_cod: bool | None = None,
        is_dressing_room: bool | None = None,
        weight_max: int | None = None,
        weight_min: int | None = None,
        length: int | None = None,
        width: int | None = None,
        height: int | None = None,
        lang: str | None = "rus",
        take_only: bool | None = None,
        is_handout: bool | None = None,
        is_reception: bool | None = None,
        is_marketplace: bool | None = None,
        is_ltl: bool | None = None,
        ltl_acceptance_partners: bool | None = None,
        ltl_issuance_partners: bool | None = None,
        fulfillment: bool | None = None,
        fias_guid: str | None = None,
        size: int | None = None,
        page: int | None = None,
    ):
        """
        Метод предназначен для получения списка действующих офисов СДЭК.

        Рекомендуем делать запрос к методу и обновлять список офисов раз в сутки для корректного отображения актуального списка ПВЗ и постаматов.

        Args:
            code (str): Код ПВЗ (пример: "NSK1")
            type (str): Тип офиса. Принимает значения "POSTAMAT", "PVZ", "ALL".
                    По умолчанию "ALL"
            postal_code (str): Почтовый индекс города
            city_code (int): Код населенного пункта СДЭК (метод "Список населенных пунктов")
            country_code (str): Код страны в формате ISO_3166-1_alpha-2 (пример: "RU")
            region_code (int): Код региона СДЭК
            have_cashless (bool): Наличие терминала оплаты.
            have_cash (bool): Есть прием наличных
            allowed_cod (bool): Разрешен наложенный платеж
            is_dressing_room (bool): Наличие примерочной
            weight_max (int): Максимальный вес в кг, который может принять офис
            weight_min (int): Минимальный вес в кг, который принимает офис
            length (int): Длина грузоместа в см
            width (int): Ширина грузоместа в см
            height (int): Высота грузоместа в см
            lang (str): Локализация офиса. По умолчанию "rus"
            take_only (bool): Является ли офис только пунктом выдачи
            is_handout (bool): Является пунктом выдачи
            is_reception (bool): Есть ли в офисе приём заказов
            is_marketplace (bool): Офис для доставки "До маркетплейса"
            is_ltl (bool): Работает ли офис с LTL (сборный груз)
            ltl_acceptance_partners (bool): Принимает заказы LTL от партнеров
            ltl_issuance_partners (bool): Выдает заказы LTL от партнеров
            fulfillment (bool): Офис с зоной фулфилмента
            fias_guid (str): Код города ФИАС (UUID)
            size (int): Ограничение выборки результата (размер страницы)
            page (int): Номер страницы выборки результата
        """

        def _convert_bool(value: bool | None) -> str | None:
            if value is None:
                return None
            return "true" if value else "false"

        params = {
            "code": code,
            "type": type,
            "postal_code": postal_code,
            "city_code": city_code,
            "country_code": country_code,
            "region_code": region_code,
            "have_cashless": _convert_bool(have_cashless),
            "have_cash": _convert_bool(have_cash),
            "allowed_cod": _convert_bool(allowed_cod),
            "is_dressing_room": _convert_bool(is_dressing_room),
            "weight_max": weight_max,
            "weight_min": weight_min,
            "length": length,
            "width": width,
            "height": height,
            "lang": lang,
            "take_only": _convert_bool(take_only),
            "is_handout": _convert_bool(is_handout),
            "is_reception": _convert_bool(is_reception),
            "is_marketplace": _convert_bool(is_marketplace),
            "is_ltl": _convert_bool(is_ltl),
            "ltl_acceptance_partners": _convert_bool(ltl_acceptance_partners),
            "ltl_issuance_partners": _convert_bool(ltl_issuance_partners),
            "fulfillment": _convert_bool(fulfillment),
            "fias_guid": fias_guid,
            "size": size,
            "page": page,
        }

        result = await self._http.request("GET", "/v2/deliverypoints", params=params)
        return result
