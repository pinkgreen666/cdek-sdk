from pydantic import BaseModel


class AvailableDeliveryIntervalDto(BaseModel):
    start_time: str
    end_time: str


class AvailableDeliveryIntervalsInfoDto(BaseModel):
    date: str
    time_intervals: list[AvailableDeliveryIntervalDto]


class GetDeliveryIntervalsResponse(BaseModel):
    date_intervals: list[AvailableDeliveryIntervalsInfoDto]


class ScheduleLocationDto(BaseModel):
    code: int | None = None
    city_uuid: str | None = None
    city: str | None = None
    fias_guid: str | None = None
    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    address: str | None = None
    postal_code: str | None = None


class RootEntityDto(BaseModel):
    uuid: str


class ErrorDto1(BaseModel):
    code: str
    additional_code: str | None = None
    message: str


class WarningDto(BaseModel):
    code: str
    message: str


class RequestDto1(BaseModel):
    request_uuid: str | None = None
    type: str
    date_time: str
    state: str
    errors: list[ErrorDto1] | None
    warnings: list[WarningDto]


class RelatedEntityDto(BaseModel):
    uuid: str
    type: str
    url: str | None = None
    create_time: str | None = None
    cdek_number: str | None = None
    date: str | None = None
    time_from: str | None = None
    time_to: str | None = None


class PostDeliveryResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto1]
    realted_entities: list[RelatedEntityDto] | None = None


class ScheduleStatusDto(BaseModel):
    code: str
    name: str
    date_time: str


class ScheduleInfoDto(BaseModel):
    cdek_number: str | None = None
    order_uuid: str
    date: str
    time_from: str
    time_to: str
    comment: str | None = None
    delivery_point: str | None = None
    to_location: ScheduleLocationDto | None = None
    uuid: str
    statuses: list[ScheduleStatusDto]
    source: str | None = None


class GetDeliveryUuidResponse(BaseModel):
    entity: ScheduleInfoDto | None = None
    requests: list[RequestDto1]
    related_entities: list[RelatedEntityDto] | None = None


class EstimatedDeliveryIntervalsRequestToLocationDto(BaseModel):
    code: int | None = None
    fias_guid: str | None = None
    postal_code: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    country_code: str | None = None
    region: str | None = None
    region_code: int | None = None
    sub_region: str | None = None
    city: str | None = None
    address: str


class EstimatedDeliveryIntervalsRequestFromLocationDto(BaseModel):
    code: int | None = None
    fias_guid: str | None = None
    postal_code: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    country_code: str | None = None
    region: str | None = None
    region_code: int | None = None
    sub_region: str | None = None
    city: str | None = None
    address: str


class EstimatedDeliveryIntervalDto(BaseModel):
    start_time: str | None = None
    end_time: str | None = None
    agreed_count: int | None = None
    total_count: int | None = None


class EstimatedDeliveryIntervalsInfoDto(BaseModel):
    date: str | None = None
    time_intervals: list[EstimatedDeliveryIntervalDto]


class PostDeliveryEstimatedIntervalsResponse(BaseModel):
    date_intervals: list[EstimatedDeliveryIntervalsInfoDto]
