from pydantic import BaseModel


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


class RestrictionItemrequestDto(BaseModel):
    name: str | None = None
    amount: int | None = None
    item_id: str | None = None
    feacn_code: str | None = None


class RestrictionPackageRequestDto(BaseModel):
    weight: int | None = None
    length: int | None = None
    width: int | None = None
    height: int | None = None
    items: list[RestrictionItemrequestDto] | None = None
    package_id: str | None = None


class ErrorDto(BaseModel):
    code: str
    additional_code: str | None = None
    message: str


class WarningDto(BaseModel):
    code: str
    message: str


class HintReasonDto(BaseModel):
    code: str | None = None
    name: str | None = None


class HintStatusDto(BaseModel):
    code: str | None = None
    name: str | None = None
    reason: HintReasonDto | None = None


class ItemHintDto(BaseModel):
    item_id: str | None = None
    feacn_code: str | None = None
    status: HintStatusDto
    limitations: list[str]
    documents: list[str]


class PackageHintDto(BaseModel):
    package_id: str | None = None
    status: HintStatusDto | None = None
    desctiption: str | None = None
    items: list[ItemHintDto] | None = None


class InternationalPackageRestictionResponse(BaseModel):
    errors: list[ErrorDto] | None = None
    warnings: list[WarningDto] | None = None
    packages: list[PackageHintDto] | None = None
