import pytest

from cdek.models.calculator import (
    CalcAdditionalServiceDto,
    CalcPackageRequestDto,
    CalculatorLocationDto,
    TariffListResponse,
    TariffResponse,
    AllTariffsResponse,
    TariffAndServiceResponse,
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

    assert isinstance(result, TariffListResponse)
    assert len(result.tariff_codes) > 0


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
    assert len(tarifflist.tariff_codes) > 0, (
        "Expected at least one tariff in calculator/tarifflist response"
    )
    tariff_code = tarifflist.tariff_codes[0].tariff_code

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

    assert isinstance(result, TariffResponse)
    assert result.delivery_sum is not None or result.errors is not None


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

    assert isinstance(result, TariffAndServiceResponse)
    assert len(result.tariff_codes) > 0


@pytest.mark.asyncio
async def test_get_calculator_alltariffs(live_client, cdek_response_printer):
    result = await live_client.calculator.get_calculator_alltariffs()
    cdek_response_printer("calculator/alltariffs", result)

    assert isinstance(result, AllTariffsResponse)
    assert len(result.tariff_codes) > 0
