from typing import Literal
from ..models.calculator import (
    CalcAdditionalServiceDto,
    CalcPackageRequestDto,
    CalculatorLocationDto,
    TariffListResponse,
    TariffResponse,
    AllTariffsResponse,
    TariffAndServiceResponse,
)
from ..http.async_http import AsyncHTTPClient


class CalculatorService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_calculator_tarifflist(
        self,
        from_location: CalculatorLocationDto,
        to_location: CalculatorLocationDto,
        packages: list[CalcPackageRequestDto],
        date: str | None = None,
        type: Literal[1, 2] | None = None,
        additional_order_types: list[int] | None = None,
        currency: int | None = None,
        lang: Literal["rus", "eng", "zho"] | None = None,
    ) -> TariffListResponse:
        """
        Метод используется клиентами для расчета стоимости и сроков доставки по всем доступным тарифам.

        Args:
            date (str | None): Дата и время планируемой передачи заказа. По умолчанию - текущая
            type (int | None): Тип заказа.
                        1 - интернет-магазин,
                        2 - доставка.
                        По умолчанию - 1
            additional_order_types (list[int] | None): Дополнительный тип заказа:
                                                2 - для сборного груза (LTL). Совместим с типом заказа "ИМ"/"Доставка";
                                                4 - для Форвард (Forward). Совместим с типом заказа "ИМ";
                                                6 - для "Фулфилмент. Приход". Совместим с типом заказа "ИМ"/"Доставка";
                                                7 - для "Фулфилмент. Отгрузка". Совместим с типом заказа "ИМ";
                                                9 - для Форвард. Экспресс (Forward. Express). Совместим с типом заказа "ИМ";
                                                10 - для доставки шин по тарифу "Экономичный экспресс". Совместим с типом заказа "ИМ"/"Доставка";
                                                11 - для доставки в рамках одного офиса "Один офис" (при условии, что офис отправителя и получателя совпадают). Совместим с типом заказа "ИМ"/"Доставка";
                                                14 - для CDEK.Shopping. Совместим с типом заказа "ИМ";
                                                15 - для "ТО для последней мили". Совместим с типом заказа "ИМ"/"Доставка".
            currency (int | None): Валюта, в которой необходимо произвести расчет (числовой код из "Приложение 14. Код валюты для методов расчета стоимости").
                            По умолчанию - валюта договора
            lang (str | None): Язык вывода информации о тарифах.
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
            "packages": [package.dict(exclude_none=True) for package in packages],
        }

        result = await self._http.request(
            "POST", "/v2/calculator/tarifflist", json=request_data
        )
        return TariffListResponse(**result)

    async def post_calculator_tariff(
        self,
        tariff_code: int,
        from_location: CalculatorLocationDto,
        to_location: CalculatorLocationDto,
        services: list[CalcAdditionalServiceDto],
        packages: list[CalcPackageRequestDto],
        additional_order_types: list[int] | None = None,
        date: str | None = None,
        type: Literal[1, 2] | None = None,
        currency: int | None = None,
        lang: Literal["rus", "eng", "zho"] | None = None,
    ) -> TariffResponse:
        """
        Метод используется для расчета стоимости и сроков доставки по конкретному коду тарифа
        по указанному направлению с учетом весо-габаритных характеристик груза.
        В ответе предоставляется информация о доступных тарифах, их стоимости и сроках доставки.
        В данном методе возможно произвести расчет стоимость доставки с учетом стоимости дополнительных услуг.

        Args:
            date (int | None): Дата и время планируемой передачи заказа. По умолчанию - текущая
            type (int | None): Тип заказа.
                        1 - интернет-магазин,
                        2 - доставка.
                        По умолчанию - 1
            currency (int | None): Валюта, в которой необходимо произвести расчет (числовой код из "Приложение 14. Код валюты для методов расчета стоимости").
                            По умолчанию - валюта договора
            lang (str | None): Язык вывода информации о тарифах.
                        Возможные значения: rus, eng, zho.
                        По умолчанию - rus
            tariff_code (int): Код тарифа. Обязателен для расчета по коду тарифа
            from_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            to_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            services (list[CalcAdditionalServiceDto]): Дополнительные услуги
            packages (CalcPackageRequestDto): Места (упаковки) в заказе
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
        """
        request_data = {
            "date": date,
            "type": type,
            "currency": currency,
            "lang": lang,
            "tariff_code": tariff_code,
            "from_location": from_location.dict(exclude_none=True),
            "to_location": to_location.dict(exclude_none=True),
            "services": [service.dict(exclude_none=True) for service in services],
            "packages": [package.dict(exclude_none=True) for package in packages],
            "additional_order_types": additional_order_types,
        }

        result = await self._http.request(
            "POST", "/v2/calculator/tariff", json=request_data
        )

        return TariffResponse(**result)

    async def post_calculator_tariffandservice(
        self,
        from_location: CalculatorLocationDto,
        to_location: CalculatorLocationDto,
        packages: list[CalcPackageRequestDto],
        date: str | None = None,
        type: Literal[1, 2] | None = None,
        currency: int | None = None,
        lang: str | None = None,
        services: list[CalcAdditionalServiceDto] | None = None,
        additional_order_types: list[int] | None = None,
    ) -> TariffAndServiceResponse:
        """
        Метод используется клиентами для расчета стоимости и сроков доставки по доступным тарифам,
        с учётом переданных дополнительных услуг.

        Args:
            date (str | None): Дата и время планируемой передачи заказа. По умолчанию - текущая
            type (int | None): Тип заказа.
                        1 - интернет-магазин,
                        2 - доставка.
                        По умолчанию - 1
            currency (int | None): Валюта, в которой необходимо произвести расчет (числовой код из "Приложение 14. Код валюты для методов расчета стоимости").
                            По умолчанию - валюта договора
            lang (str | None): Язык вывода информации о тарифах.
                        Возможные значения: rus, eng, zho.
                        По умолчанию - rus
            from_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            to_location (CalculatorLocationDto): Населённый пункт для вычислений тарифа
            services (list[CalcAdditionalServiceDto] | None): Дополнительные услуги
            packages (list[CalcPackageRequestDto]): Места (упаковки) в заказе
            additional_order_types (list[int] | None): Дополнительный тип заказа:
                                                2 - для сборного груза (LTL). Совместим с типом заказа "ИМ"/"Доставка";
                                                4 - для Форвард (Forward). Совместим с типом заказа "ИМ";
                                                6 - для "Фулфилмент. Приход". Совместим с типом заказа "ИМ"/"Доставка";
                                                7 - для "Фулфилмент. Отгрузка". Совместим с типом заказа "ИМ";
                                                9 - для Форвард. Экспресс (Forward. Express). Совместим с типом заказа "ИМ";
                                                10 - для доставки шин по тарифу "Экономичный экспресс". Совместим с типом заказа "ИМ"/"Доставка";
                                                11 - для доставки в рамках одного офиса "Один офис" (при условии, что офис отправителя и получателя совпадают). Совместим с типом заказа "ИМ"/"Доставка";
                                                14 - для CDEK.Shopping. Совместим с типом заказа "ИМ";
                                                15 - для "ТО для последней мили". Совместим с типом заказа "ИМ"/"Доставка".
        """
        request_data = {
            "date": date,
            "type": type,
            "currency": currency,
            "lang": lang,
            "from_location": from_location.dict(exclude_none=True),
            "to_location": to_location.dict(exclude_none=True),
            "services": (
                [service.dict(exclude_none=True) for service in services]
                if services is not None
                else None
            ),
            "packages": [package.dict(exclude_none=True) for package in packages],
            "additional_order_types": additional_order_types,
        }

        result = await self._http.request(
            "POST", "/v2/calculator/tariffAndService", json=request_data
        )

        return TariffAndServiceResponse(**result)

    async def get_calculator_alltariffs(self) -> AllTariffsResponse:
        """
        Метод позволяет получить список всех доступных и актуальных тарифов по договору.
        """
        result = await self._http.request("GET", "/v2/calculator/alltariffs")

        return AllTariffsResponse(**result)
