"""
Пример скачивания квитанции в PDF файл.
Файл будет сохранен в текущей директории.
"""

import asyncio
import os
from pathlib import Path

from cdek import CdekClient
from cdek.models.print import PrintOrderDto
from cdek.models.order import (
    RecipientContactDto,
    PhoneDto,
    PackageRequestDto,
    ItemRequestDto,
    MoneyDto,
)


async def download_waybill_example():
    """Создает заказ, формирует квитанцию и скачивает PDF"""
    client_id = os.getenv("CDEK_CLIENT_ID")
    client_secret = os.getenv("CDEK_CLIENT_SECRET")

    client = CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    )

    try:
        print("=== Шаг 1: Создание заказа ===")

        recipient = RecipientContactDto(
            name="Иванов Иван Иванович",
            phones=[PhoneDto(number="+79001234567")]
        )

        item = ItemRequestDto(
            name="Тестовый товар",
            ware_key="TEST-001",
            payment=MoneyDto(value=5000.0),
            weight=2000,
            amount=1,
            cost=5000.0
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
            number=f"ORDER-{int(asyncio.get_event_loop().time())}",
            shipment_point="MSK1",
            delivery_point="SPB1",
        )

        print(f"✓ Заказ создан с UUID: {order.entity.uuid}")

        # Ждем обработки заказа
        print("\nОжидание обработки заказа (5 сек)...")
        await asyncio.sleep(5)

        print("\n=== Шаг 2: Формирование квитанции ===")

        print_order = PrintOrderDto(order_uuid=order.entity.uuid)

        waybill = await client.print.post_print_orders(
            orders=[print_order],
            copy_count=2,
            type="tpl_russia"
        )

        waybill_uuid = waybill.entity.uuid
        print(f"✓ Квитанция создана с UUID: {waybill_uuid}")

        # Ждем формирования квитанции
        print("\nОжидание формирования квитанции (10 сек)...")
        await asyncio.sleep(10)

        print("\n=== Шаг 3: Проверка статуса квитанции ===")

        waybill_info = await client.print.get_print_orders_uuid(waybill_uuid)

        if waybill_info.entity.statuses:
            for status in waybill_info.entity.statuses:
                print(f"  {status.code}: {status.name} ({status.date_time})")

            latest_status = waybill_info.entity.statuses[-1]

            if latest_status.code == "READY":
                print("\n=== Шаг 4: Скачивание PDF ===")

                # Скачиваем PDF
                pdf_content = await client.print.get_print_orders_uuidpdf(waybill_uuid)

                # Сохраняем в текущую директорию
                filename = f"waybill_{waybill_uuid}.pdf"
                filepath = Path.cwd() / filename

                with open(filepath, "wb") as f:
                    f.write(pdf_content)

                print(f"✓ PDF скачан успешно!")
                print(f"  Размер файла: {len(pdf_content):,} байт")
                print(f"  Путь к файлу: {filepath}")
                print(f"\nОткройте файл командой:")
                print(f"  xdg-open {filepath}")

                return filepath
            else:
                print(f"\n⚠ Квитанция еще не готова. Текущий статус: {latest_status.code}")
                print("Попробуйте позже или увеличьте время ожидания")
        else:
            print("\n⚠ Нет информации о статусе квитанции")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(download_waybill_example())
