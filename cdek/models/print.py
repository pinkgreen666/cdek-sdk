from pydantic import BaseModel


class PrintOrderDto(BaseModel):
    order_uuid: str
    cdek_number: str | None = None


class PrintOrdersRequest(BaseModel):
    orders: list[PrintOrderDto]
    copy_count: int = 2
    type: str | None = None


class WaybillStatusDto(BaseModel):
    code: str
    name: str | None = None
    date_time: str | None = None


class WaybillDto(BaseModel):
    uuid: str
    url: str | None = None
    statuses: list[WaybillStatusDto] | None = None


class ErrorDto(BaseModel):
    code: str
    additional_code: str | None = None
    message: str


class WarningDto(BaseModel):
    code: str
    message: str


class RequestDto(BaseModel):
    request_uuid: str | None = None
    type: str
    date_time: str
    state: str
    errors: list[ErrorDto] | None = None
    warnings: list[WarningDto] | None = None


class RelatedEntityDto(BaseModel):
    uuid: str
    type: str
    url: str | None = None
    create_time: str | None = None
    cdek_number: str | None = None
    date: str | None = None
    time_from: str | None = None
    time_to: str | None = None


class PrintOrdersResponse(BaseModel):
    entity: WaybillDto | None = None
    requests: list[RequestDto]
    related_entities: list[RelatedEntityDto] | None = None


class GetWaybillResponse(BaseModel):
    entity: WaybillDto
    requests: list[RequestDto]
    related_entities: list[RelatedEntityDto] | None = None
