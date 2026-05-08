from cdek.models.international import (
    InternationalPackageRestictionResponse,
    LocationDto,
    RestrictionPackageRequestDto,
)
from ..http.async_http import AsyncHTTPClient


class InternationalService:
    def __init__(self, http_client: AsyncHTTPClient):
        self._http = http_client

    async def post_international_package_restriction(
        self,
        tariff_code: int | None = None,
        from_location: LocationDto | None = None,
        to_location: LocationDto | None = None,
        packages: list[RestrictionPackageRequestDto] | None = None,
    ) -> InternationalPackageRestictionResponse:
        request_data = {
            "tariff_code": tariff_code,
            "from_location": from_location.dict(exclude_none=True)
            if from_location
            else None,
            "to_location": to_location.dict(exclude_none=True) if to_location else None,
            "packages": [package.dict(exclude_none=True) for package in packages]
            if packages
            else None,
        }

        result = await self._http.request(
            "POST", "/v2/international/package/restrictions", json=request_data
        )
        return InternationalPackageRestictionResponse(**result)
