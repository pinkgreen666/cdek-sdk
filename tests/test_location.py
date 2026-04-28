import pytest


@pytest.mark.asyncio
async def test_get_location_suggest_cities(live_client, cdek_response_printer):
    result = await live_client.location.get_location_suggest_cities(
        name="Москва", country_code="RU"
    )
    cdek_response_printer("location/suggest/cities", result)

    assert isinstance(result, list)
    assert result


@pytest.mark.asyncio
async def test_get_location_regions(live_client, cdek_response_printer):
    result = await live_client.location.get_location_regions(
        country_codes="RU", size=5, page=0, lang="rus"
    )
    cdek_response_printer("location/regions", result)

    assert isinstance(result, list)
    assert result


@pytest.mark.asyncio
async def test_get_location_postalcodes(live_client, cdek_response_printer):
    result = await live_client.location.get_location_postalcodes(city_code=44)
    cdek_response_printer("location/postalcodes", result)

    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_location_coordinates(live_client, cdek_response_printer):
    result = await live_client.location.get_location_coordinates(
        latitude=55.7558, longitude=37.6173
    )
    cdek_response_printer("location/cooridnates", result)

    assert result is None or isinstance(result, (dict, list))


@pytest.mark.asyncio
async def test_get_location_cities(live_client, cdek_response_printer):
    result = await live_client.location.get_location_cities(
        city="Москва", country_codes="RU", size=5, page=0, lang="rus"
    )
    cdek_response_printer("location/cities", result)

    assert isinstance(result, list)
    assert result
