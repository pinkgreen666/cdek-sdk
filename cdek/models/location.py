from pydantic import BaseModel


class SuggestCitiesResponseSchema(BaseModel):
    city_uuid: str
    code: int
    full_name: str
    country_code: str


class RegionsResponseSchema(BaseModel):
    country_code: str
    country: str
    region: str
    region_code: int | None = None
    kladr_region_code: str | None = None


class PostalCodesResponseSchema(BaseModel):
    code: int
    postal_codes: list[str]


class CoordinatesResponseSchema(BaseModel):
    code: int
    city_uuid: str
    city: str
    fias_guid: str | None = None


class CitiesResponseSchema(BaseModel):
    code: int
    city_uuid: str
    city: str
    fias_guid: str | None = None
    country_code: str
    country: str
    region: str
    region_code: int | None = None
    sub_region: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    time_zone: str | None = None
    payment_limit: float
