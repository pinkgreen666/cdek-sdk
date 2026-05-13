from cdek.models.delivery import (
    AvailableDeliveryIntervalsInfoDto,
    EstimatedDeliveryIntervalsRequestFromLocationDto,
    EstimatedDeliveryIntervalsRequestToLocationDto,
    GetDeliveryIntervalsResponse,
    GetDeliveryUuidResponse,
    PostDeliveryEstimatedIntervalsResponse,
    PostDeliveryResponse,
    ScheduleLocationDto,
)
from ..http.async_http import AsyncHTTPClient


class DeliveryService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def get_delivery_intervals(
        self, cdek_number: str | None = None, order_uuid: str | None = None
    ) -> GetDeliveryIntervalsResponse:
        params = {
            "cdek_number": cdek_number,
            "order_uuid": order_uuid,
        }

        result = await self._http.request(
            "GET", "/v2/delivery/intervals", params=params
        )

        return GetDeliveryIntervalsResponse(**result)

    async def post_delivery(
        self,
        date: str,
        cdek_number: str | None = None,
        order_uuid: str | None = None,
        time_from: str | None = None,
        time_to: str | None = None,
        comment: str | None = None,
        delivery_point: str | None = None,
        to_location: ScheduleLocationDto | None = None,
    ) -> PostDeliveryResponse:
        request_data = {
            "cdek_number": cdek_number,
            "order_uuid": order_uuid,
            "date": date,
            "time_from": time_from,
            "time_to": time_to,
            "comment": comment,
            "delivery_point": delivery_point,
            "to_location": to_location.dict(exclude_none=True) if to_location else None,
        }

        result = await self._http.request("POST", "/v2/delivery", json=request_data)

        return PostDeliveryResponse(**result)

    async def get_delivery_uuid(self, uuid: str) -> GetDeliveryUuidResponse:
        result = await self._http.request("GET", f"/v2/delivery/{uuid}")

        return GetDeliveryUuidResponse(**result)

    async def post_delivery_estimatedintervals(
        self,
        date_time: str,
        to_location: EstimatedDeliveryIntervalsRequestToLocationDto,
        tariff_code: int,
        from_location: EstimatedDeliveryIntervalsRequestFromLocationDto | None = None,
        shipment_point: str | None = None,
        additional_order_types: list[int] | None = None,
    ) -> PostDeliveryEstimatedIntervalsResponse:
        request_data = {
            "date_time": date_time,
            "from_location": from_location.dict(exclude_none=True)
            if from_location
            else None,
            "shipment_point": shipment_point,
            "to_location": to_location.dict(exclude_none=True),
            "tariff_code": tariff_code,
            "additional_order_types": additional_order_types,
        }

        result = await self._http.request(
            "POST", "/v2/delivery/estimatedIntervals", json=request_data
        )

        return PostDeliveryEstimatedIntervalsResponse(**result)
