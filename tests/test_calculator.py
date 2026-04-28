import pytest

from cdek.models.calculator import (
    CalcAdditionalServiceDto,
    CalcPackageRequestDto,
    CalculatorLocationDto,
)


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


@pytest.mark.asyncio
async def test_post_calculator_tariff(live_client, cdek_response_printer):
    from_location = CalculatorLocationDto(code=44)
    to_location = CalculatorLocationDto(code=137)
    packages = [CalcPackageRequestDto(weight=1000, length=10, width=10, height=10)]

    tarifflist = await live_client.calculator.post_calculator_tarifflist(
        from_location=from_location,
        to_location=to_location,
        packages=packages,
        type=1,
        currency=1,
        lang="rus",
    )
    tariff_codes = (tarifflist or {}).get("tariff_codes") or []
    assert tariff_codes, (
        "Expected at least one tariff in calculator/tarifflist response"
    )
    tariff_code = tariff_codes[0]["tariff_code"]

    result = await live_client.calculator.post_calculator_tariff(
        tariff_code=tariff_code,
        from_location=from_location,
        to_location=to_location,
        services=[],
        packages=packages,
        additional_order_types=[],
        type=1,
        currency=1,
        lang="rus",
    )
    cdek_response_printer("calculator/tariff", result)

    assert isinstance(result, dict)
    assert "errors" in result or "tariff_code" in result or "delivery_sum" in result


@pytest.mark.asyncio
async def test_post_calculator_tariffandservice(live_client, cdek_response_printer):
    from_location = CalculatorLocationDto(code=44)
    to_location = CalculatorLocationDto(code=137)
    packages = [CalcPackageRequestDto(weight=1000, length=10, width=10, height=10)]

    result = await live_client.calculator.post_calculator_tariffandservice(
        from_location=from_location,
        to_location=to_location,
        packages=packages,
        type=1,
        currency=1,
        lang="rus",
        services=[CalcAdditionalServiceDto(code="INSURANCE", parameter="1000")],
        additional_order_types=None,
    )
    cdek_response_printer("calculator/tariffAndService", result)

    assert isinstance(result, dict)
    assert "tariff_codes" in result or "errors" in result


@pytest.mark.asyncio
async def test_get_calculator_alltariffs(live_client, cdek_response_printer):
    result = await live_client.calculator.get_calculator_alltariffs()
    cdek_response_printer("calculator/alltariffs", result)

    assert isinstance(result, dict)
    assert isinstance(result.get("tariff_codes"), list)
    assert result["tariff_codes"]
