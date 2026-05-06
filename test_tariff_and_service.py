#!/usr/bin/env python3
"""
Тест метода post_calculator_tariffandservice
"""
import asyncio
import json
from cdek import CdekClient
from cdek.models.calculator import (
    CalculatorLocationDto,
    CalcPackageRequestDto,
    CalcAdditionalServiceDto,
)

# Тестовые учетные данные
CLIENT_ID = "wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP"
CLIENT_SECRET = "RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5"


async def test_without_services():
    """Тест БЕЗ дополнительных услуг"""
    print("\n" + "=" * 80)
    print("ТЕСТ 1: Расчет БЕЗ дополнительных услуг (post_calculator_tarifflist)")
    print("=" * 80)

    client = CdekClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        test_mode=True,
    )

    from_location = CalculatorLocationDto(code=44)  # Москва
    to_location = CalculatorLocationDto(code=137)  # Санкт-Петербург
    packages = [
        CalcPackageRequestDto(
            weight=1000,
            length=30,
            width=20,
            height=10
        )
    ]

    result = await client.calculator.post_calculator_tarifflist(
        from_location=from_location,
        to_location=to_location,
        packages=packages,
        type=1,
        lang="rus",
    )

    print(f"\nКоличество тарифов: {len(result.tariff_codes)}")
    print("\nПервые 3 тарифа:")
    for i, tariff in enumerate(result.tariff_codes[:3]):
        print(f"\n{i+1}. Тариф {tariff.tariff_code}:")
        print(f"   Название: {tariff.tariff_name}")
        print(f"   Описание: {tariff.tariff_description}")
        print(f"   Режим доставки: {tariff.delivery_mode}")
        print(f"   Стоимость: {tariff.delivery_sum}")
        print(f"   Срок: {tariff.period_min}-{tariff.period_max} дней")

    await client.close()
    return result


async def test_with_services():
    """Тест С дополнительными услугами"""
    print("\n" + "=" * 80)
    print("ТЕСТ 2: Расчет С дополнительными услугами (post_calculator_tariffandservice)")
    print("=" * 80)

    client = CdekClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        test_mode=True,
    )

    from_location = CalculatorLocationDto(code=44)  # Москва
    to_location = CalculatorLocationDto(code=137)  # Санкт-Петербург
    packages = [
        CalcPackageRequestDto(
            weight=1000,
            length=30,
            width=20,
            height=10
        )
    ]
    services = [
        CalcAdditionalServiceDto(
            code="INSURANCE",
            parameter="5000"
        )
    ]

    result = await client.calculator.post_calculator_tariffandservice(
        from_location=from_location,
        to_location=to_location,
        packages=packages,
        services=services,
        type=1,
        lang="rus",
    )

    print(f"\nКоличество тарифов: {len(result.tariff_codes)}")
    print("\nПервые 3 успешных тарифа:")

    success_count = 0
    for i, tariff in enumerate(result.tariff_codes):
        if tariff.status == "true" and success_count < 3:
            success_count += 1
            print(f"\n{success_count}. Тариф {tariff.tariff_code}:")
            print(f"   Статус: {tariff.status}")
            print(f"   Стоимость доставки: {tariff.result.delivery_sum}")
            print(f"   Срок: {tariff.result.period_min}-{tariff.result.period_max} дней")
            print(f"   Итоговая стоимость (с услугами): {tariff.result.total_sum}")
            if tariff.result.services:
                print(f"   Услуги:")
                for svc in tariff.result.services:
                    print(f"     - {svc.code}: {svc.total_sum} руб")
        elif tariff.status == "false":
            if tariff.result.errors:
                print(f"\n❌ Тариф {tariff.tariff_code}: {tariff.result.errors[0].message}")

    await client.close()
    return result


async def test_with_multiple_services():
    """Тест с несколькими услугами"""
    print("\n" + "=" * 80)
    print("ТЕСТ 3: Расчет с НЕСКОЛЬКИМИ услугами (INSURANCE + SMS)")
    print("=" * 80)

    client = CdekClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        test_mode=True,
    )

    from_location = CalculatorLocationDto(code=44)
    to_location = CalculatorLocationDto(code=137)
    packages = [
        CalcPackageRequestDto(
            weight=1000,
            length=30,
            width=20,
            height=10
        )
    ]
    services = [
        CalcAdditionalServiceDto(code="INSURANCE", parameter="5000"),
        CalcAdditionalServiceDto(code="SMS", parameter=""),
    ]

    result = await client.calculator.post_calculator_tariffandservice(
        from_location=from_location,
        to_location=to_location,
        packages=packages,
        services=services,
        type=1,
        lang="rus",
    )

    print(f"\nКоличество тарифов: {len(result.tariff_codes)}")

    success_count = 0
    error_count = 0
    for tariff in result.tariff_codes:
        if tariff.status == "true":
            success_count += 1
        else:
            error_count += 1

    print(f"Успешных: {success_count}, С ошибками: {error_count}")

    await client.close()
    return result


async def main():
    print("Начинаем тестирование методов калькулятора CDEK SDK")
    print(f"Время: {asyncio.get_event_loop().time()}")

    try:
        # Тест без услуг
        result1 = await test_without_services()

        # Тест с услугами
        result2 = await test_with_services()

        # Тест с несколькими услугами
        result3 = await test_with_multiple_services()

        print("\n" + "=" * 80)
        print("СРАВНЕНИЕ РЕЗУЛЬТАТОВ:")
        print("=" * 80)
        print(f"Без услуг: {len(result1.tariff_codes)} тарифов")
        print(f"С услугой INSURANCE: {len(result2.tariff_codes)} тарифов")
        print(f"С услугами INSURANCE + SMS: {len(result3.tariff_codes)} тарифов")

        # Подсчет успешных тарифов
        success_count2 = sum(1 for t in result2.tariff_codes if t.status == "true")
        success_count3 = sum(1 for t in result3.tariff_codes if t.status == "true")

        print(f"\nУспешных расчетов с INSURANCE: {success_count2}")
        print(f"Успешных расчетов с INSURANCE + SMS: {success_count3}")

        if success_count2 > 0:
            print("\n✅ API корректно возвращает данные с услугами!")
            print("✅ SDK теперь правильно парсит ответ!")
        else:
            print("\n⚠️  Все тарифы вернули ошибки")

        print("\n" + "=" * 80)
        print("Тестирование завершено")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
