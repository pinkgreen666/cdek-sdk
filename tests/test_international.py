import pytest

from cdek.models.international import (
    InternationalPackageRestictionResponse,
    LocationDto,
    RestrictionItemrequestDto,
    RestrictionPackageRequestDto,
)


@pytest.mark.asyncio
async def test_post_international_package_restriction_basic(
    live_client, cdek_response_printer
):
    pytest.skip(
        "Skipping test: CDEK test API returns 500 Internal Error for international/package/restrictions endpoint"
    )

    from_location = LocationDto(code=44, country_code="RU", city="Москва")
    to_location = LocationDto(code=162, country_code="KZ", city="Алматы")

    packages = [
        RestrictionPackageRequestDto(
            weight=1000,
            length=10,
            width=10,
            height=10,
            package_id="pkg1",
            items=[
                RestrictionItemrequestDto(
                    name="Тестовый товар",
                    amount=1,
                    item_id="item1",
                    feacn_code="1234567890",
                )
            ],
        )
    ]

    result = await live_client.international.post_international_package_restriction(
        tariff_code=7,
        from_location=from_location,
        to_location=to_location,
        packages=packages,
    )
    cdek_response_printer("international/package/restrictions", result)

    assert isinstance(result, InternationalPackageRestictionResponse)


@pytest.mark.asyncio
async def test_post_international_package_restriction_multiple_items(
    live_client, cdek_response_printer
):
    pytest.skip(
        "Skipping test: CDEK test API returns 500 Internal Error for international/package/restrictions endpoint"
    )

    from_location = LocationDto(code=137, country_code="RU", city="Санкт-Петербург")
    to_location = LocationDto(code=1644, country_code="BY", city="Минск")

    packages = [
        RestrictionPackageRequestDto(
            weight=2000,
            length=20,
            width=15,
            height=10,
            package_id="pkg1",
            items=[
                RestrictionItemrequestDto(
                    name="Товар 1",
                    amount=2,
                    item_id="item1",
                    feacn_code="1111111111",
                ),
                RestrictionItemrequestDto(
                    name="Товар 2",
                    amount=1,
                    item_id="item2",
                    feacn_code="2222222222",
                ),
            ],
        )
    ]

    result = await live_client.international.post_international_package_restriction(
        tariff_code=7,
        from_location=from_location,
        to_location=to_location,
        packages=packages,
    )
    cdek_response_printer("international/package/restrictions multiple items", result)

    assert isinstance(result, InternationalPackageRestictionResponse)


@pytest.mark.asyncio
async def test_post_international_package_restriction_multiple_packages(
    live_client, cdek_response_printer
):
    pytest.skip(
        "Skipping test: CDEK test API returns 500 Internal Error for international/package/restrictions endpoint"
    )

    from_location = LocationDto(code=270, country_code="RU", city="Новосибирск")
    to_location = LocationDto(code=1645, country_code="KG", city="Бишкек")

    packages = [
        RestrictionPackageRequestDto(
            weight=1000,
            length=10,
            width=10,
            height=10,
            package_id="pkg1",
            items=[
                RestrictionItemrequestDto(
                    name="Товар в посылке 1",
                    amount=1,
                    item_id="item1",
                    feacn_code="1234567890",
                )
            ],
        ),
        RestrictionPackageRequestDto(
            weight=1500,
            length=15,
            width=12,
            height=8,
            package_id="pkg2",
            items=[
                RestrictionItemrequestDto(
                    name="Товар в посылке 2",
                    amount=1,
                    item_id="item2",
                    feacn_code="0987654321",
                )
            ],
        ),
    ]

    result = await live_client.international.post_international_package_restriction(
        tariff_code=7,
        from_location=from_location,
        to_location=to_location,
        packages=packages,
    )
    cdek_response_printer("international/package/restrictions multiple packages", result)

    assert isinstance(result, InternationalPackageRestictionResponse)


@pytest.mark.asyncio
async def test_post_international_package_restriction_minimal(
    live_client, cdek_response_printer
):
    pytest.skip(
        "Skipping test: CDEK test API returns 500 Internal Error for international/package/restrictions endpoint"
    )

    from_location = LocationDto(code=44, country_code="RU")
    to_location = LocationDto(code=162, country_code="KZ")

    packages = [
        RestrictionPackageRequestDto(
            weight=500,
            package_id="pkg1",
            items=[
                RestrictionItemrequestDto(
                    name="Минимальный товар",
                    item_id="item1",
                    feacn_code="1111111111",
                )
            ],
        )
    ]

    result = await live_client.international.post_international_package_restriction(
        tariff_code=7,
        from_location=from_location,
        to_location=to_location,
        packages=packages,
    )
    cdek_response_printer("international/package/restrictions minimal", result)

    assert isinstance(result, InternationalPackageRestictionResponse)
