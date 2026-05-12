import pytest
import asyncio

from cdek.models.print import (
    PrintOrderDto,
    PrintOrdersResponse,
    GetWaybillResponse,
)


@pytest.mark.asyncio
async def test_create_waybill_for_order(live_client, cdek_response_printer):
    """Test creating waybill (receipt) for an order"""
    import time
    from cdek.models.order import (
        RecipientContactDto,
        PhoneDto,
        PackageRequestDto,
        ItemRequestDto,
        MoneyDto,
    )

    # Step 1: Create an order first
    order_number = f"TEST-WAYBILL-{int(time.time())}"

    recipient = RecipientContactDto(
        name="Тестовый Получатель Квитанция",
        phones=[PhoneDto(number="+79007777777")]
    )

    item = ItemRequestDto(
        name="Тестовый товар для квитанции",
        ware_key="TEST-WAYBILL-001",
        payment=MoneyDto(value=3000.0),
        weight=1500,
        amount=1,
        cost=3000.0
    )

    package = PackageRequestDto(
        number="1",
        weight=1500,
        items=[item]
    )

    create_result = await live_client.order.post_orders(
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )

    assert create_result.entity is not None
    order_uuid = create_result.entity.uuid
    print(f"\nCreated order with UUID: {order_uuid}")

    # Wait for order to be processed
    print("Waiting 5 seconds for order to be processed...")
    await asyncio.sleep(5)

    # Step 2: Create waybill for the order
    print_order = PrintOrderDto(order_uuid=order_uuid)

    waybill_result = await live_client.print.post_print_orders(
        orders=[print_order],
        copy_count=2,
        type="tpl_russia"
    )
    cdek_response_printer("print/create_waybill", waybill_result)

    assert isinstance(waybill_result, PrintOrdersResponse)
    assert waybill_result.requests is not None
    assert len(waybill_result.requests) > 0

    # Check if entity is present (may be None initially)
    if waybill_result.entity:
        waybill_uuid = waybill_result.entity.uuid
        print(f"\nWaybill UUID: {waybill_uuid}")
    else:
        # Extract UUID from requests if entity is not present
        request = waybill_result.requests[0]
        assert request.request_uuid is not None
        waybill_uuid = request.request_uuid
        print(f"\nWaybill request UUID: {waybill_uuid}")


@pytest.mark.asyncio
async def test_get_waybill_by_uuid(live_client, cdek_response_printer):
    """Test getting waybill by UUID and checking its status"""
    import time
    from cdek.models.order import (
        RecipientContactDto,
        PhoneDto,
        PackageRequestDto,
        ItemRequestDto,
        MoneyDto,
    )

    # Step 1: Create an order
    order_number = f"TEST-WAYBILL-GET-{int(time.time())}"

    recipient = RecipientContactDto(
        name="Тестовый Получатель Получение Квитанции",
        phones=[PhoneDto(number="+79008888888")]
    )

    item = ItemRequestDto(
        name="Тестовый товар для получения квитанции",
        ware_key="TEST-WAYBILL-GET-001",
        payment=MoneyDto(value=2500.0),
        weight=1200,
        amount=1,
        cost=2500.0
    )

    package = PackageRequestDto(
        number="1",
        weight=1200,
        items=[item]
    )

    create_result = await live_client.order.post_orders(
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )

    assert create_result.entity is not None
    order_uuid = create_result.entity.uuid
    print(f"\nCreated order with UUID: {order_uuid}")

    # Wait for order to be processed
    print("Waiting 5 seconds for order to be processed...")
    await asyncio.sleep(5)

    # Step 2: Create waybill
    print_order = PrintOrderDto(order_uuid=order_uuid)

    waybill_result = await live_client.print.post_print_orders(
        orders=[print_order],
        copy_count=2,
    )

    assert waybill_result.requests is not None
    assert len(waybill_result.requests) > 0

    # Get waybill UUID
    if waybill_result.entity:
        waybill_uuid = waybill_result.entity.uuid
    else:
        request = waybill_result.requests[0]
        assert request.request_uuid is not None
        waybill_uuid = request.request_uuid

    print(f"\nWaybill UUID: {waybill_uuid}")

    # Step 3: Wait for waybill to be generated
    print("Waiting 10 seconds for waybill to be generated...")
    await asyncio.sleep(10)

    # Step 4: Get waybill by UUID
    get_result = await live_client.print.get_print_orders_uuid(waybill_uuid)
    cdek_response_printer("print/get_waybill_by_uuid", get_result)

    assert isinstance(get_result, GetWaybillResponse)
    assert get_result.entity is not None
    assert get_result.entity.uuid == waybill_uuid

    # Check statuses
    if get_result.entity.statuses:
        print(f"\nWaybill statuses:")
        for status in get_result.entity.statuses:
            print(f"  - {status.code}: {status.name} at {status.date_time}")

        # Check if waybill is ready
        status_codes = [s.code for s in get_result.entity.statuses]
        if "READY" in status_codes:
            assert get_result.entity.url is not None
            print(f"\nWaybill is ready! Download URL: {get_result.entity.url}")
            print("Note: URL is valid for 1 hour")
        elif "PROCESSING" in status_codes:
            print("\nWaybill is still being generated")
        elif "ACCEPTED" in status_codes:
            print("\nWaybill request has been accepted")


@pytest.mark.asyncio
async def test_create_waybill_multiple_orders(live_client, cdek_response_printer):
    """Test creating waybill for multiple orders at once"""
    import time
    from cdek.models.order import (
        RecipientContactDto,
        PhoneDto,
        PackageRequestDto,
        ItemRequestDto,
        MoneyDto,
    )

    order_uuids = []

    # Create 2 orders
    for i in range(2):
        order_number = f"TEST-MULTI-WAYBILL-{int(time.time())}-{i}"

        recipient = RecipientContactDto(
            name=f"Тестовый Получатель {i+1}",
            phones=[PhoneDto(number=f"+7900999999{i}")]
        )

        item = ItemRequestDto(
            name=f"Тестовый товар {i+1}",
            ware_key=f"TEST-MULTI-{i+1}",
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

        create_result = await live_client.order.post_orders(
            tariff_code=136,
            recipient=recipient,
            packages=[package],
            number=order_number,
            shipment_point="MSK1",
            delivery_point="SPB1",
        )

        assert create_result.entity is not None
        order_uuids.append(create_result.entity.uuid)
        print(f"\nCreated order {i+1} with UUID: {create_result.entity.uuid}")

        # Small delay between order creations
        await asyncio.sleep(2)

    # Wait for orders to be processed
    print("\nWaiting 5 seconds for orders to be processed...")
    await asyncio.sleep(5)

    # Create waybill for multiple orders
    print_orders = [PrintOrderDto(order_uuid=uuid) for uuid in order_uuids]

    waybill_result = await live_client.print.post_print_orders(
        orders=print_orders,
        copy_count=2,
        type="tpl_russia"
    )
    cdek_response_printer("print/create_waybill_multiple", waybill_result)

    assert isinstance(waybill_result, PrintOrdersResponse)
    assert waybill_result.requests is not None
    print(f"\nCreated waybill for {len(print_orders)} orders")


@pytest.mark.asyncio
async def test_create_waybill_with_different_templates(live_client, cdek_response_printer):
    """Test creating waybills with different template types"""
    import time
    from cdek.models.order import (
        RecipientContactDto,
        PhoneDto,
        PackageRequestDto,
        ItemRequestDto,
        MoneyDto,
    )

    # Create an order
    order_number = f"TEST-TEMPLATE-{int(time.time())}"

    recipient = RecipientContactDto(
        name="Тестовый Получатель Шаблоны",
        phones=[PhoneDto(number="+79001111111")]
    )

    item = ItemRequestDto(
        name="Тестовый товар для шаблонов",
        ware_key="TEST-TEMPLATE-001",
        payment=MoneyDto(value=1800.0),
        weight=900,
        amount=1,
        cost=1800.0
    )

    package = PackageRequestDto(
        number="1",
        weight=900,
        items=[item]
    )

    create_result = await live_client.order.post_orders(
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )

    assert create_result.entity is not None
    order_uuid = create_result.entity.uuid

    # Wait for order to be processed
    await asyncio.sleep(5)

    # Test different template types
    templates = ["tpl_russia", "tpl_english", "tpl_china"]

    for template in templates:
        print(f"\nTesting template: {template}")
        print_order = PrintOrderDto(order_uuid=order_uuid)

        waybill_result = await live_client.print.post_print_orders(
            orders=[print_order],
            copy_count=2,
            type=template
        )

        assert isinstance(waybill_result, PrintOrdersResponse)
        assert waybill_result.requests is not None
        print(f"Successfully created waybill with template: {template}")

        # Small delay between requests
        await asyncio.sleep(2)

    cdek_response_printer("print/create_waybill_templates", waybill_result)


@pytest.mark.asyncio
async def test_download_waybill_pdf(live_client, cdek_response_printer):
    """Test downloading waybill PDF file"""
    import time
    from pathlib import Path
    from cdek.models.order import (
        RecipientContactDto,
        PhoneDto,
        PackageRequestDto,
        ItemRequestDto,
        MoneyDto,
    )

    # Create tests/tmp directory if it doesn't exist
    tmp_dir = Path(__file__).parent / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    # Step 1: Create an order
    order_number = f"TEST-DOWNLOAD-{int(time.time())}"

    recipient = RecipientContactDto(
        name="Тестовый Получатель Скачивание",
        phones=[PhoneDto(number="+79002222222")]
    )

    item = ItemRequestDto(
        name="Тестовый товар для скачивания",
        ware_key="TEST-DOWNLOAD-001",
        payment=MoneyDto(value=3500.0),
        weight=1800,
        amount=1,
        cost=3500.0
    )

    package = PackageRequestDto(
        number="1",
        weight=1800,
        items=[item]
    )

    create_result = await live_client.order.post_orders(
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )

    assert create_result.entity is not None
    order_uuid = create_result.entity.uuid
    print(f"\nCreated order with UUID: {order_uuid}")

    # Wait for order to be processed
    await asyncio.sleep(5)

    # Step 2: Create waybill
    print_order = PrintOrderDto(order_uuid=order_uuid)

    waybill_result = await live_client.print.post_print_orders(
        orders=[print_order],
        copy_count=2,
        type="tpl_russia"
    )

    assert waybill_result.entity is not None
    waybill_uuid = waybill_result.entity.uuid
    print(f"Waybill UUID: {waybill_uuid}")

    # Step 3: Wait for waybill to be ready
    print("Waiting 10 seconds for waybill to be generated...")
    await asyncio.sleep(10)

    # Step 4: Check if waybill is ready
    get_result = await live_client.print.get_print_orders_uuid(waybill_uuid)

    if get_result.entity.statuses:
        latest_status = get_result.entity.statuses[-1]
        print(f"Waybill status: {latest_status.code}")

        if latest_status.code == "READY":
            # Step 5: Download PDF
            pdf_content = await live_client.print.get_print_orders_uuidpdf(waybill_uuid)

            assert isinstance(pdf_content, bytes)
            assert len(pdf_content) > 0
            assert pdf_content[:4] == b'%PDF'  # PDF magic number

            # Save to tests/tmp directory
            pdf_file = tmp_dir / f"waybill_{waybill_uuid}.pdf"
            with open(pdf_file, "wb") as f:
                f.write(pdf_content)

            print(f"\n✓ PDF downloaded successfully!")
            print(f"File size: {len(pdf_content)} bytes")
            print(f"Saved to: {pdf_file}")

            cdek_response_printer("print/download_pdf", {
                "waybill_uuid": waybill_uuid,
                "file_size": len(pdf_content),
                "file_path": str(pdf_file)
            })
        else:
            print(f"\n⏳ Waybill not ready yet, status: {latest_status.code}")
            print("Skipping PDF download test")
    else:
        print("\n⚠ No status information available")
        print("Skipping PDF download test")
