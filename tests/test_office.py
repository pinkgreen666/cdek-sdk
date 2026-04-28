import pytest


@pytest.mark.asyncio
async def test_get_deliverypoints(live_client, cdek_response_printer):
    result = await live_client.office.get_deliverypoints(
        city_code=44,
        have_cashless=True,
        size=5,
        page=0,
    )
    cdek_response_printer("deliverypoints", result)

    assert isinstance(result, list)
    assert result
