from pydantic import BaseModel
from pydantic.typing import NONE_TYPES


class AccompanyingWaybillDto(BaseModel):
    client_name: str
    flight_number: str | None = None
    air_waybil_numbers: list[str] | None = None
    vehicle_numbers: list[str] | None = None
    planned_departure_date_time: str | None = None


class DeliveryRecipientCostResponseDto(BaseModel):
    value: float
    vat_sum: float | None = None
    vat_rate: int | None = None


class DeliveryCostThresholdDto(BaseModel):
    threshold: int | None = None
    sum: float | None = None
    vat_sum: float | None = None
    vat_rate: int | None = None


class PhoneDto(BaseModel):
    number: str
    additional: str | None = None


class SenderResponseContactDto(BaseModel):
    company: str | None = None
    name: str
    contragent_type: str | None = None
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    tin: str | None = None
    passport_date_of_birth: str | None = None
    email: str | None = None
    phones: list[PhoneDto]
    passport_requrements_satisfied: str | None = None


class SellerDto(BaseModel):
    name: str | None = None
    inn: str | None = None
    phone: str | None = None
    ownership_form: str | None = None
    address: str | None = None


class RecipientResponseContactDto(BaseModel):
    company: str | None = None
    name: str
    contragent_type: str | None = None
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    tin: str | None = None
    passport_date_of_birth: str | None = None
    email: str | None = None
    phones: list[PhoneDto]
    passport_requrements_satisfied: str | None = None


class ResponseFromLocationDto(BaseModel):
    code: int
    city_uuid: str | None = None
    city: str
    fias_guid: str | None = None
    country_code: str
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    fias_region_guid: str | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    time_zone: str | None = None
    payment_limit: float | None = None
    address: str | None = None
    postal_code: str | None = None


class ResponseToLocationDto(BaseModel):
    code: int
    city_uuid: str | None = None
    city: str
    fias_guid: str | None = None
    country_code: str
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    fias_region_guid: str | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    time_zone: str | None = None
    payment_limit: float | None = None
    address: str | None = None
    postal_code: str | None = None


class AdditionalServiceResponseDto(BaseModel):
    code: str | None = None
    parameter: str | None = None
    sum: float | None = None
    total_sum: float | None = None
    discount_percent: float | None = None
    vat_rate: float | None = None
    vat_sum: float | None = None


class ResponseMoneyDto(BaseModel):
    value: float
    vat_sum: float | None = None
    vat_rate: int | None = None


class SellerItemDto(BaseModel):
    name: str | None = None
    inn: str | None = None
    phone: str | None = None
    ownership_from: str | None = None
    address: str | None = None
    giis_subdivision_id: str | None = None


class ReturnItemDetail(BaseModel):
    direct_order_number: str | None = None
    direct_order_uuid: str | None = None
    direct_package_number: str | None = None


class ItemResponseDto(BaseModel):
    name: str
    ware_key: str
    marking: str | None = None
    payment: ResponseMoneyDto
    weight: int
    weight_gross: int | None = None
    amount: int
    delivery_amount: int | None = None
    mane_i18n: str | None = None
    brand: str | None = None
    country_code: str | None = None
    material: str | None = None
    wifi_gsm: str | None = None
    url: str | None = None
    seller: SellerItemDto | None = None
    return_item_detail: ReturnItemDetail | None = None
    excise: str | None = None
    cost: float
    feach_code: str | None = None
    jewel_uin: str | None = None
    used: str | None = None


class PackageAddServiceResponseDto(BaseModel):
    code: str


class PackageResponseDto(BaseModel):
    number: str
    barcode: str | None = None
    weight: int
    length: int | None = None
    width: int | None = None
    weight_volumne: int | None = None
    weight_calc: int | None = None
    height: int | None = None
    comment: str | None = None
    items: list[ItemResponseDto] | None = None
    services: list[PackageAddServiceResponseDto] | None = None
    package_id: str | None = None


class OrderStatusDto(BaseModel):
    code: str | None = None
    name: str | None = None
    date_time: str | None = None
    reason_code: str | None = None
    city: str | None = None
    city_uuid: str | None = None
    deleted: str | None = None


class OrderDelayReason(BaseModel):
    create_date: str | None = None
    description: str | None = None


class ReponsePaymentTypeDto(BaseModel):
    type: str
    sum: str


class ResponseDeliveryDetailDto(BaseModel):
    date: str | None = None
    recipient_name: str | None = None
    payment_sum: float | None = None
    delivery_sum: float
    total_sum: float
    payment_info: list[ReponsePaymentTypeDto] | None = None
    delivery_vat_rate: float | None = None
    delivery_vat_sum: float | None = None
    delivery_discount_percent: float | None = None
    delivery_discount_sum: float | None = None


class DeliveryProblemResponseDto(BaseModel):
    code: str | None = None
    create_date: str | None = None


class FailedCallResponseDto(BaseModel):
    date_time: str
    reason_code: int


class RescheduledCallResponseDto(BaseModel):
    date_time: str
    date_next: str
    time_next: str
    comment: str | None = None


class CallsResponseDto(BaseModel):
    field_calls: list[FailedCallResponseDto] | None = None
    rescheduled_calls: list[RescheduledCallResponseDto] | None = None


class OrderResponseDto(BaseModel):
    uuid: str
    type: int
    additional_order_types: list[int] | None = None
    is_return: str
    is_reverse: str
    cdek_number: str | None = None
    number: str | None = None
    accompanying_number: str | None = None
    accompanying_waybill: AccompanyingWaybillDto | None = None
    tariff_code: int
    comment: str | None = None
    shipment_point: str | None = None
    delivery_point: str | None = None
    date_invoice: str | None = None
    keep_free_until: str | None = None
    shipper_name: str | None = None
    shipper_address: str | None = None
    delivery_recipient_cost: DeliveryRecipientCostResponseDto
    delivery_recipient_cost_adv: DeliveryCostThresholdDto | None = None
    sender: SenderResponseContactDto
    seller: SellerDto | None = None
    recipient: RecipientResponseContactDto
    from_location: ResponseFromLocationDto
    to_location: ResponseToLocationDto
    services: list[AdditionalServiceResponseDto]
    packages: list[PackageResponseDto]
    statuses: list[OrderStatusDto]
    is_client_return: str
    delivery_mode: str | None = None
    has_reverse_order: str | None = None
    delay_reasons: list[OrderDelayReason] | None = None
    planned_delivery_date: str | None = None
    delivery_detail: ResponseDeliveryDetailDto | None = None
    delivery_problem: list[DeliveryProblemResponseDto] | None = None
    developer_key: str | None = None
    calls: CallsResponseDto | None = None


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


class GetOrdersResponse(BaseModel):
    entity: OrderResponseDto | None = None
    requests: list[RequestDto]
    related_entities: list[RelatedEntityDto] | None = None


class RecipientContactDto(BaseModel):
    company: str | None = None
    name: str
    contragent_type: str | None = None
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    tin: str | None = None
    passport_date_of_birth: str | None = None
    email: str | None = None
    phones: list[PhoneDto] | None = None


class MoneyDto(BaseModel):
    value: float
    vat_sum: float | None = None
    vat_rate: int | None = None


class ItemRequestDto(BaseModel):
    name: str
    ware_key: str
    marking: str | None = None
    payment: MoneyDto
    weight: int
    weight_gross: int | None = None
    amount: int
    name_i18n: str | None = None
    brand: str | None = None
    country_code: str | None = None
    material: str | None = None
    wifi_gsm: str | None = None
    url: str | None = None
    seller: SellerItemDto | None = None
    cost: float
    feach_code: str | None = None
    jewel_uin: str | None = None
    used: str | None = None


class PackageRequestDto(BaseModel):
    number: str
    weight: int
    length: int | None = None
    width: int | None = None
    height: int | None = None
    comment: str | None = None
    items: list[ItemRequestDto] | None = None
    package_id: str | None = None


class DeliveryRecipientCostRequestDto(BaseModel):
    value: float
    vat_sum: float | None = None
    vat_rate: int | None = None


class SenderContactDto(BaseModel):
    compnay: str | None = None
    name: str
    contragent_type: str | None = None
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    tin: str | None = None
    passport_date_of_birth: str | None = None
    email: str | None = None
    phones: list[PhoneDto]


class RequestFromLocationDto(BaseModel):
    code: int | None = None
    city_uuid: str | None = None
    city: str | None = None
    fias_guid: str | None = None
    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    fias_region_guid: str | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    time_zone: str | None = None
    payment_limit: float | None = None
    address: str
    postal_code: str | None


class RequestToLocationDto(BaseModel):
    code: int | None = None
    city_uuid: str | None = None
    city: str | None = None
    fias_guid: str | None = None
    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    fias_region_guid: str | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    time_zone: str | None = None
    payment_limit: float | None = None
    address: str
    postal_code: str | None


class AdditionalServiceRequestDto(BaseModel):
    code: str | None = None
    parameter: str | None = None


class RootEntityDto(BaseModel):
    uuid: str


class PostOrdersResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto]
    related_entities: list[RelatedEntityDto] | None = None


class LocationDto(BaseModel):
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
    time_zone: str | None = None
    payment_limit: float | None = None
    address: str | None = None
    postal_code: str | None = None


class ErrorDto1(BaseModel):
    code: str
    additional_code: str | None = None
    message: str


class RequestDto1(BaseModel):
    request_uuid: str | None = None
    type: str
    date_time: str
    state: str
    errors: list[ErrorDto1] | None
    warnings: list[WarningDto]


class PatchOrdersResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto1]
    related_entities: list[RelatedEntityDto] | None = None


class DeleteOrdersResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto1]
    related_entities: list[RelatedEntityDto] | None = None


class ContactDto(BaseModel):
    company: str | None = None
    name: str
    contragent_type: str | None = None
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    tin: str | None = None
    passport_date_of_birth: str | None = None
    email: str | None = None
    phones: list[PhoneDto] | None = None
    passport_requrements_satisfied: str | None = None


class LocationInfoDto(BaseModel):
    code: int | None = None
    city_uuid: str | None = None
    city: str | None = None
    fias_guid: str | None = None
    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    sub_region: str | None = None
    longitude: str | None = None
    latitude: str | None = None
    address: str | None = None
    postal_code: str | None = None


class IntakeStatusDto(BaseModel):
    code: str
    name: str
    date_time: str


class IntakePackageDto(BaseModel):
    package_id: str | None = None
    weight: int | None = None
    length: int | None = None
    width: int | None = None
    height: int | None = None


class GetOrdersIntakesResponse(BaseModel):
    uuid: str
    cdek_number: str | None = None
    order_uuid: str | None = None
    intake_date: str
    intake_number: str | None = None
    intake_time_from: str
    intake_time_to: str
    lunch_time_from: str | None = None
    lunch_time_to: str | None = None
    name: str | None = None
    weight: int | None = None
    length: int | None = None
    width: int | None = None
    height: int | None = None
    comment: str | None = None
    courier_power_of_attomey: str | None = None
    courier_identity_card: str | None = None
    sender: ContactDto | None = None
    from_location: LocationInfoDto
    to_location: LocationInfoDto | None = None
    need_call: str | None = None
    statuses: list[IntakeStatusDto]
    packages: list[IntakePackageDto] | None = None


class PostOrdersRefusalResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto1]
    realted_entities: list[RelatedEntityDto] | None = None


class PostOrdersClientReturnResponse(BaseModel):
    entity: RootEntityDto | None = None
    requests: list[RequestDto1]
    related_entities: list[RelatedEntityDto] | None = None
