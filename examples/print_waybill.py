"""
Примеры использования Print Service для формирования квитанций к заказам.

Этот модуль демонстрирует:
- Создание квитанции для одного заказа
- Создание квитанции для нескольких заказов
- Получение ссылки на готовую квитанцию
- Использование различных шаблонов квитанций
- Проверку статуса формирования квитанции
"""

import asyncio
import os

from cdek import CdekClient
from cdek.models.print import PrintOrderDto
from cdek.models.order import (
    RecipientContactDto,
    PhoneDto,
    PackageRequestDto,
    ItemRequestDto,
    MoneyDto,
)


async def create_waybill_for_single_order():
    """Создание квитанции для одного заказа"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    async with CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    ) as client:
        # Сначала создаем заказ
        recipient = RecipientContactDto(
            name="Иванов Иван Иванович",
            phones=[PhoneDto(number="+79001234567")]
        )

        item = ItemRequestDto(
            name="Ноутбук",
            ware_key="LAPTOP-001",
            payment=MoneyDto(value=50000.0),
            weight=2000,
            amount=1,
            cost=50000.0
        )

        package = PackageRequestDto(
            number="1",
            weight=2000,
            items=[item]
        )

        order = await client.order.post_orders(
            tariff_code=136,
            recipient=recipient,
            packages=[package],
            number="ORDER-12345",
            shipment_point="MSK1",
            delivery_point="SPB1",
        )

        print(f"Создан заказ с UUID: {order.entity.uuid}")

        # Ждем обработки заказа
        await asyncio.sleep(5)

        # Создаем квитанцию
        print_order = PrintOrderDto(order_uuid=order.entity.uuid)

        waybill = await client.print.post_print_orders(
            orders=[print_order],
            copy_count=2,  # 2 копии на листе
            type="tpl_russia"  # Русский шаблон
        )

        print(f"Квитанция создана с UUID: {waybill.entity.uuid}")
        print(f"Статус запроса: {waybill.requests[0].state}")

        return waybill.entity.uuid


async def get_waybill_download_link(waybill_uuid: str):
    """Получение ссылки на скачивание квитанции"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    async with CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    ) as client:
        # Ждем формирования квитанции
        print("Ожидание формирования квитанции...")
        await asyncio.sleep(10)

        # Получаем информацию о квитанции
        waybill = await client.print.get_print_orders_uuid(waybill_uuid)

        print(f"\nИнформация о квитанции:")
        print(f"UUID: {waybill.entity.uuid}")

        if waybill.entity.statuses:
            print("\nСтатусы:")
            for status in waybill.entity.statuses:
                print(f"  - {status.code}: {status.name} ({status.date_time})")

            # Проверяем, готова ли квитанция
            status_codes = [s.code for s in waybill.entity.statuses]

            if "READY" in status_codes:
                print(f"\n✓ Квитанция готова!")
                print(f"Ссылка для скачивания: {waybill.entity.url}")
                print("Внимание: ссылка действительна в течение 1 часа")
            elif "PROCESSING" in status_codes:
                print("\n⏳ Квитанция формируется...")
            elif "ACCEPTED" in status_codes:
                print("\n⏳ Запрос принят в обработку...")
            elif "INVALID" in status_codes:
                print("\n✗ Некорректный запрос")
            elif "REMOVED" in status_codes:
                print("\n✗ Срок действия ссылки истек")


async def create_waybill_for_multiple_orders():
    """Создание одной квитанции для нескольких заказов"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    async with CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    ) as client:
        order_uuids = []

        # Создаем несколько заказов
        for i in range(3):
            recipient = RecipientContactDto(
                name=f"Получатель {i+1}",
                phones=[PhoneDto(number=f"+7900123456{i}")]
            )

            item = ItemRequestDto(
                name=f"Товар {i+1}",
                ware_key=f"ITEM-{i+1}",
                payment=MoneyDto(value=1000.0 * (i+1)),
                weight=500 * (i+1),
                amount=1,
                cost=1000.0 * (i+1)
            )

            package = PackageRequestDto(
                number="1",
                weight=500 * (i+1),
                items=[item]
            )

            order = await client.order.post_orders(
                tariff_code=136,
                recipient=recipient,
                packages=[package],
                number=f"ORDER-MULTI-{i+1}",
                shipment_point="MSK1",
                delivery_point="SPB1",
            )

            order_uuids.append(order.entity.uuid)
            print(f"Создан заказ {i+1} с UUID: {order.entity.uuid}")

            await asyncio.sleep(2)

        # Ждем обработки заказов
        await asyncio.sleep(5)

        # Создаем одну квитанцию для всех заказов
        print_orders = [PrintOrderDto(order_uuid=uuid) for uuid in order_uuids]

        waybill = await client.print.post_print_orders(
            orders=print_orders,
            copy_count=2
        )

        print(f"\nСоздана общая квитанция для {len(print_orders)} заказов")
        print(f"UUID квитанции: {waybill.entity.uuid}")


async def create_waybill_with_different_templates():
    """Создание квитанций с различными шаблонами"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    async with CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    ) as client:
        # Создаем заказ
        recipient = RecipientContactDto(
            name="Тестовый Получатель",
            phones=[PhoneDto(number="+79001234567")]
        )

        item = ItemRequestDto(
            name="Тестовый товар",
            ware_key="TEST-001",
            payment=MoneyDto(value=2000.0),
            weight=1000,
            amount=1,
            cost=2000.0
        )

        package = PackageRequestDto(
            number="1",
            weight=1000,
            items=[item]
        )

        order = await client.order.post_orders(
            tariff_code=136,
            recipient=recipient,
            packages=[package],
            number="ORDER-TEMPLATES",
            shipment_point="MSK1",
            delivery_point="SPB1",
        )

        print(f"Создан заказ с UUID: {order.entity.uuid}")
        await asyncio.sleep(5)

        # Доступные шаблоны
        templates = {
            "tpl_russia": "Русский",
            "tpl_english": "Английский",
            "tpl_china": "Китайский",
            "tpl_armenia": "Армянский",
            "tpl_italian": "Итальянский",
            "tpl_korean": "Корейский",
            "tpl_latvian": "Латышский",
            "tpl_lithuanian": "Литовский",
            "tpl_german": "Немецкий",
            "tpl_turkish": "Турецкий",
            "tpl_czech": "Чешский",
            "tpl_thailand": "Тайский",
            "tpl_invoice": "Инвойс",
        }

        print_order = PrintOrderDto(order_uuid=order.entity.uuid)

        # Создаем квитанцию с русским шаблоном
        waybill = await client.print.post_print_orders(
            orders=[print_order],
            copy_count=2,
            type="tpl_russia"
        )

        print(f"\nСоздана квитанция с шаблоном 'Русский'")
        print(f"UUID: {waybill.entity.uuid}")

        print("\nДоступные шаблоны:")
        for code, name in templates.items():
            print(f"  - {code}: {name}")


async def check_waybill_status_with_polling(waybill_uuid: str, max_attempts: int = 10):
    """Проверка статуса квитанции с опросом до готовности"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    async with CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    ) as client:
        for attempt in range(max_attempts):
            print(f"\nПопытка {attempt + 1}/{max_attempts}...")

            waybill = await client.print.get_print_orders_uuid(waybill_uuid)

            if waybill.entity.statuses:
                latest_status = waybill.entity.statuses[-1]
                print(f"Текущий статус: {latest_status.code} - {latest_status.name}")

                if latest_status.code == "READY":
                    print(f"\n✓ Квитанция готова!")
                    print(f"Ссылка: {waybill.entity.url}")
                    return waybill.entity.url
                elif latest_status.code == "INVALID":
                    print("\n✗ Ошибка формирования квитанции")
                    return None

            # Ждем перед следующей попыткой
            await asyncio.sleep(3)

        print("\n⏱ Превышено максимальное время ожидания")
        return None


async def main():
    """Главная функция с примерами"""
    print("=== Пример 1: Создание квитанции для одного заказа ===")
    waybill_uuid = await create_waybill_for_single_order()

    print("\n=== Пример 2: Получение ссылки на квитанцию ===")
    await get_waybill_download_link(waybill_uuid)

    print("\n=== Пример 3: Создание квитанции для нескольких заказов ===")
    await create_waybill_for_multiple_orders()

    print("\n=== Пример 4: Различные шаблоны квитанций ===")
    await create_waybill_with_different_templates()

    print("\n=== Пример 5: Проверка статуса с опросом ===")
    await check_waybill_status_with_polling(waybill_uuid)


if __name__ == "__main__":
    asyncio.run(main())
