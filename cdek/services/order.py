from cdek.models.order import (
    AdditionalServiceRequestDto,
    DeliveryCostThresholdDto,
    DeliveryRecipientCostRequestDto,
    GetOrdersResponse,
    PackageRequestDto,
    PostOrdersResponse,
    RecipientContactDto,
    RequestFromLocationDto,
    RequestToLocationDto,
    SellerDto,
    SenderContactDto,
)
from ..http.async_http import AsyncHTTPClient


class OrderService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_orders(
        self, cdek_number: int | None = None, im_number: str | None = None
    ) -> GetOrdersResponse:
        params = {"cdek_number": cdek_number, "im_number": im_number}

        result = await self._http.request("GET", "/v2/orders", params=params)

        return GetOrdersResponse(**result)

    async def post_orders(
        self,
        tariff_code: int,
        recipient: RecipientContactDto,
        packages: list[PackageRequestDto],
        type: int | None = None,
        additional_order_types: int | None = None,
        number: str | None = None,
        accompanying_number: str | None = None,
        comment: str | None = None,
        shipment_point: str | None = None,
        delivery_point: str | None = None,
        date_invoice: str | None = None,
        shipper_name: str | None = None,
        shipper_address: str | None = None,
        delivery_recipient_cost: DeliveryRecipientCostRequestDto | None = None,
        delivery_recipient_cost_adv: DeliveryCostThresholdDto | None = None,
        sender: SenderContactDto | None = None,
        seller: SellerDto | None = None,
        from_location: RequestFromLocationDto | None = None,
        to_location: RequestToLocationDto | None = None,
        services: list[AdditionalServiceRequestDto] | None = None,
        is_client_return: str | None = None,
        has_reverse_order: str | None = None,
        developer_key: str | None = None,
        print: str | None = None,
        widget_token: str | None = None,
    ) -> PostOrdersResponse:
        request_data = {
            "type": type,
            "additional_order_types": additional_order_types,
            "number": number,
            "accompanying_number": accompanying_number,
            "tariff_code": tariff_code,
            "comment": comment,
            "shipment_point": shipment_point,
            "delivery_point": delivery_point,
            "date_invoice": date_invoice,
            "shipper_name": shipper_name,
            "shipper_address": shipper_address,
            "delivery_recipient_cost": delivery_recipient_cost.dict(exclude_none=True)
            if delivery_recipient_cost
            else None,
            "delivery_recipient_cost_adv": delivery_recipient_cost_adv.dict(
                exclude_none=True
            )
            if delivery_recipient_cost_adv
            else None,
            "sender": sender.dict(exclude_none=True) if sender else None,
            "seller": seller.dict(exclude_none=True) if seller else None,
            "recipient": recipient.dict(exclude_none=True),
            "from_location": from_location.dict(exclude_none=True)
            if from_location
            else None,
            "to_location": to_location.dict(exclude_none=True) if to_location else None,
            "services": [service.dict(exclude_none=True) for service in services]
            if services
            else None,
            "packages": [package.dict(exclude_none=True) for package in packages],
            "is_client_return": is_client_return,
            "has_reverse_order": has_reverse_order,
            "developer_key": developer_key,
            "print": print,
            "widget_token": widget_token,
        }

        result = await self._http.request("POST", "/v2/orders", json=request_data)

        return PostOrdersResponse(**result)

    async def patch_orders(self): ...

    async def get_orders_uuid(self): ...

    async def delete_orders_uuid(self): ...

    async def get_orders_orderuuid_intakes(self): ...

    async def post_orders_uuid_refusal(self): ...

    async def post_orders_uuid_clientreturn(self): ...
