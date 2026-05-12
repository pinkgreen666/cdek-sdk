from ..http.async_http import AsyncHTTPClient
from ..models.print import (
    PrintOrderDto,
    PrintOrdersRequest,
    PrintOrdersResponse,
    GetWaybillResponse,
)


class PrintService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_print_orders(
        self,
        orders: list[PrintOrderDto],
        copy_count: int = 2,
        type: str | None = None,
    ) -> PrintOrdersResponse:
        """
        Формирование квитанции к заказу в формате PDF.

        Args:
            orders: Список заказов (максимум 100)
            copy_count: Число копий одной квитанции на листе (по умолчанию 2)
            type: Форма квитанции (tpl_china, tpl_armenia, tpl_russia, tpl_english,
                  tpl_italian, tpl_korean, tpl_latvian, tpl_lithuanian, tpl_german,
                  tpl_turkish, tpl_czech, tpl_thailand, tpl_invoice)

        Returns:
            PrintOrdersResponse с uuid запроса для последующего получения квитанции
        """
        request_data = PrintOrdersRequest(
            orders=orders,
            copy_count=copy_count,
            type=type,
        )

        response = await self._http.request(
            "POST",
            "/v2/print/orders",
            json=request_data.dict(exclude_none=True),
        )

        return PrintOrdersResponse(**response)

    async def get_print_orders_uuid(self, uuid: str) -> GetWaybillResponse:
        """
        Получение ссылки на квитанцию к заказу в формате PDF.
        Ссылка доступна в течение 1 часа.

        Args:
            uuid: Идентификатор запроса на формирование квитанции

        Returns:
            GetWaybillResponse со ссылкой на скачивание PDF и статусами
        """
        response = await self._http.request(
            "GET",
            f"/v2/print/orders/{uuid}",
        )

        return GetWaybillResponse(**response)

    async def get_print_orders_uuidpdf(self, uuid: str) -> bytes:
        """
        Скачивание готовой квитанции в формате PDF.

        Args:
            uuid: Идентификатор запроса на формирование квитанции

        Returns:
            bytes: Содержимое PDF файла

        Raises:
            CdekError: Если квитанция еще не готова или произошла ошибка
        """
        token = await self._http._ensure_token()

        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = await self._http._client.get(
            f"{self._http.base_url}/v2/print/orders/{uuid}.pdf",
            headers=headers,
        )

        if response.status_code == 401:
            await self._http._auth()
            token = await self._http._ensure_token()
            headers["Authorization"] = f"Bearer {token}"
            response = await self._http._client.get(
                f"{self._http.base_url}/v2/print/orders/{uuid}.pdf",
                headers=headers,
            )

        response.raise_for_status()
        return response.content

    async def post_print_barcodes(self): ...

    async def get_print_barcodes_uuid(self): ...

    async def get_print_barcodes_uuidpdf(self): ...
