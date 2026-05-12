import pytest

from cdek.models.order import (
    GetOrdersResponse,
    PostOrdersResponse,
    RecipientContactDto,
    PhoneDto,
    PackageRequestDto,
    ItemRequestDto,
    MoneyDto,
    SenderContactDto,
    RequestFromLocationDto,
    RequestToLocationDto,
    AdditionalServiceRequestDto,
    DeliveryRecipientCostRequestDto,
)


@pytest.mark.asyncio
async def test_get_orders_by_cdek_number(live_client, cdek_response_printer):
    """Test getting order by CDEK number (expects validation error for non-existent order)"""
    from cdek.exceptions import CdekValidationError

    cdek_number = 1234567890  # Non-existent order number

    try:
        result = await live_client.order.get_orders(cdek_number=cdek_number)
        cdek_response_printer("order/get_by_cdek_number", result)
        assert isinstance(result, GetOrdersResponse)
        assert result.requests is not None
    except CdekValidationError as e:
        # Expected for non-existent order
        assert e.status_code == 400
        assert "not_found" in str(e.response_data).lower() or "not found" in e.message.lower()


@pytest.mark.asyncio
async def test_get_orders_by_im_number(live_client, cdek_response_printer):
    """Test getting order by IM number (expects validation error for non-existent order)"""
    from cdek.exceptions import CdekValidationError

    im_number = "TEST-ORDER-NONEXISTENT"

    try:
        result = await live_client.order.get_orders(im_number=im_number)
        cdek_response_printer("order/get_by_im_number", result)
        assert isinstance(result, GetOrdersResponse)
        assert result.requests is not None
    except CdekValidationError as e:
        # Expected for non-existent order
        assert e.status_code == 400




@pytest.mark.asyncio
async def test_create_and_get_order_by_uuid(live_client, cdek_response_printer, tmp_path):
    """Test creating order and retrieving it by UUID"""
    import time
    import json
    import asyncio

    # Step 1: Create order
    recipient = RecipientContactDto(
        name="Тестовый Получатель UUID",
        phones=[PhoneDto(number="+79005555555")]
    )

    item = ItemRequestDto(
        name="Тестовый товар для UUID",
        ware_key="TEST-UUID-001",
        payment=MoneyDto(value=1500.0),
        weight=750,
        amount=1,
        cost=1500.0
    )

    package = PackageRequestDto(
        number="1",
        weight=750,
        items=[item]
    )

    order_number = f"TEST-UUID-{int(time.time())}"

    create_result = await live_client.order.post_orders(
        tariff_code=136,  # Посылка склад-склад
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )
    cdek_response_printer("order/create_for_uuid_test", create_result)

    assert isinstance(create_result, PostOrdersResponse)
    assert create_result.entity is not None
    order_uuid = create_result.entity.uuid

    # Step 2: Save UUID to file
    uuid_file = tmp_path / "test_order_uuid.json"
    with open(uuid_file, "w") as f:
        json.dump({
            "uuid": order_uuid,
            "order_number": order_number,
            "created_at": time.time()
        }, f, indent=2)

    print(f"\nOrder UUID saved to: {uuid_file}")
    print(f"Order UUID: {order_uuid}")

    # Wait for order to be processed by CDEK system
    print("Waiting 5 seconds for order to be processed...")
    await asyncio.sleep(5)

    # Step 3: Retrieve order by UUID from file
    with open(uuid_file, "r") as f:
        saved_data = json.load(f)

    retrieved_uuid = saved_data["uuid"]

    get_result = await live_client.order.get_orders_uuid(retrieved_uuid)
    cdek_response_printer("order/get_by_uuid", get_result)

    # Step 4: Verify the retrieved order
    assert isinstance(get_result, GetOrdersResponse)
    assert get_result.entity is not None
    assert get_result.entity.uuid == order_uuid
    assert get_result.entity.number == order_number
    assert get_result.entity.recipient.name == "Тестовый Получатель UUID"
    assert len(get_result.entity.packages) == 1
    assert get_result.entity.packages[0].items[0].name == "Тестовый товар для UUID"
    assert get_result.entity.cdek_number is not None
    print(f"\nSuccessfully retrieved order with CDEK number: {get_result.entity.cdek_number}")


@pytest.mark.asyncio
async def test_get_order_by_im_number_after_creation(live_client, cdek_response_printer):
    """Test creating order and retrieving it by IM number (internal order number)"""
    import time
    import asyncio

    # Step 1: Create order with unique IM number
    order_number = f"TEST-IM-{int(time.time())}"

    recipient = RecipientContactDto(
        name="Тестовый Получатель IM",
        phones=[PhoneDto(number="+79006666666")]
    )

    item = ItemRequestDto(
        name="Тестовый товар IM",
        ware_key="TEST-IM-001",
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

    create_result = await live_client.order.post_orders(
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        number=order_number,
        shipment_point="MSK1",
        delivery_point="SPB1",
    )
    cdek_response_printer("order/create_with_im_number", create_result)

    assert isinstance(create_result, PostOrdersResponse)
    assert create_result.entity is not None

    # Wait for order to be processed
    print(f"\nCreated order with IM number: {order_number}")
    print("Waiting 5 seconds for order to be processed...")
    await asyncio.sleep(5)

    # Step 2: Retrieve order by IM number
    get_result = await live_client.order.get_orders(im_number=order_number)
    cdek_response_printer("order/get_by_im_number_after_creation", get_result)

    # Step 3: Verify the retrieved order
    assert isinstance(get_result, GetOrdersResponse)
    assert get_result.entity is not None
    assert get_result.entity.number == order_number
    assert get_result.entity.recipient.name == "Тестовый Получатель IM"
    print(f"\nSuccessfully retrieved order by IM number: {order_number}")
