from sdk.models.calculator import CalcPackageRequestDto, CalculatorLocationDto
from ..http.async_http import AsyncHTTPClient


class CalculatorService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_calculator_tarifflist(
        self,
        date: str | None,
        type: int | None,
        additional_order_types: list[int] | None,
        currency: int | None,
        lang: str | None,
        from_location: CalculatorLocationDto,
        to_location: CalculatorLocationDto,
        packages: list[CalcPackageRequestDto],
    ):
        """
        Метод используется клиентами для расчета стоимости и сроков доставки по всем доступным тарифам.

        Args:
            date (str): Дата и время планируемой передачи заказа. По умолчанию - текущая
            type (int): Тип заказа.
                        1 - интернет-магазин,
                        2 - доставка.
                        По умолчанию - 1
            additional_order_types (list[int]): Дополнительный тип заказа:
                                                2 - для сборного груза (LTL). Совместим с типом заказа "ИМ"/"Доставка";
                                                4 - для Форвард (Forward). Совместим с типом заказа "ИМ";
                                                6 - для "Фулфилмент. Приход". Совместим с типом заказа "ИМ"/"Доставка";
                                                7 - для "Фулфилмент. Отгрузка". Совместим с типом заказа "ИМ";
                                                9 - для Форвард. Экспресс (Forward. Express). Совместим с типом заказа "ИМ";
                                                10 - для доставки шин по тарифу "Экономичный экспресс". Совместим с типом заказа "ИМ"/"Доставка";
                                                11 - для доставки в рамках одного офиса "Один офис" (при условии, что офис отправителя и получателя совпадают). Совместим с типом заказа "ИМ"/"Доставка";
                                                14 - для CDEK.Shopping. Совместим с типом заказа "ИМ";
                                                15 - для "ТО для последней мили". Совместим с типом заказа "ИМ"/"Доставка".
            currency (int): Валюта, в которой необходимо произвести расчет (числовой код из "Приложение 14. Код валюты для методов расчета стоимости").
                            По умолчанию - валюта договора
            lang (str): Язык вывода информации о тарифах.
                        Возможные значения: rus, eng, zho.
                        По умолчанию - rus
            from_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            to_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            packages (list[CalcPackageRequestDto]): Места (упаковки) в заказе
        """
        request_data = {
            "date": date,
            "type": type,
            "additional_order_types": additional_order_types,
            "currency": currency,
            "lang": lang,
            "from_location": from_location.dict(exclude_none=True),
            "to_location": to_location.dict(exclude_none=True),
            "packages": [
                package.dict(exclude_none=True) for package in packages
            ],
        }

        result = await self._http.request(
            "POST", "/v2/calculator/tarifflist", json=request_data
        )
        return result

    async def post_calculator_tariff(self): ...

    async def post_calculator_tariffandservice(self): ...

    async def get_calculator_alltariffs(self): ...
