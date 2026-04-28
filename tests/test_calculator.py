import pytest

from sdk.models.calculator import CalculatorLocationDto, CalcPackageRequestDto


@pytest.mark.asyncio
async def test_post_calculator_tarifflist(live_client, cdek_response_printer):
    from_location = CalculatorLocationDto(code=44)
    to_location = CalculatorLocationDto(code=137)
    packages = [CalcPackageRequestDto(weight=1000, length=10, width=10, height=10)]

    result = await live_client.calculator.post_calculator_tarifflist(
        date=None,
        type=1,
        additional_order_types=None,
        currency=1,
        lang="rus",
        from_location=from_location,
        to_location=to_location,
        packages=packages,
    )
    cdek_response_printer("calculator/tarifflist", result)

    assert isinstance(result, dict)
    assert "tariff_codes" in result or "errors" in result
