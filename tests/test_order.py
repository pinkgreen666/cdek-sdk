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
async def test_post_orders_minimal(live_client, cdek_response_printer):
    """Test creating order with minimal required fields (warehouse to warehouse)"""
    import time

    recipient = RecipientContactDto(
        name="Иванов Иван Иванович",
        phones=[PhoneDto(number="+79001234567")]
    )

    item = ItemRequestDto(
        name="Тестовый товар",
        ware_key="TEST-001",
        payment=MoneyDto(value=1000.0),
        weight=500,
        amount=1,
        cost=1000.0
    )

    package = PackageRequestDto(
        number="1",
        weight=500,
        items=[item]
    )

    result = await live_client.order.post_orders(
        tariff_code=136,  # Посылка склад-склад
        recipient=recipient,
        packages=[package],
        number=f"TEST-MIN-{int(time.time())}",
        shipment_point="MSK1",
        delivery_point="SPB1",
    )
    cdek_response_printer("order/post_minimal", result)

    assert isinstance(result, PostOrdersResponse)
    assert result.requests is not None
    assert len(result.requests) > 0


@pytest.mark.asyncio
async def test_post_orders_full(live_client, cdek_response_printer):
    """Test creating order with all optional fields (door to door)"""
    import time

    sender = SenderContactDto(
        name="Отправитель Тест",
        phones=[PhoneDto(number="+79001111111")]
    )

    recipient = RecipientContactDto(
        name="Получатель Тест",
        email="recipient@test.com",
        phones=[PhoneDto(number="+79002222222", additional="123")]
    )

    from_location = RequestFromLocationDto(
        code=44,  # Moscow
        address="ул. Тестовая, д. 1"
    )

    to_location = RequestToLocationDto(
        code=137,  # Saint Petersburg
        address="ул. Тестовая, д. 2"
    )

    item = ItemRequestDto(
        name="Тестовый товар",
        ware_key="TEST-002",
        payment=MoneyDto(value=2000.0, vat_sum=333.33, vat_rate=20),
        weight=1000,
        weight_gross=1100,
        amount=2,
        cost=2000.0,
        brand="TestBrand",
        country_code="RU"
    )

    package = PackageRequestDto(
        number="1",
        weight=1000,
        length=30,
        width=20,
        height=10,
        comment="Хрупкое",
        items=[item]
    )

    services = [
        AdditionalServiceRequestDto(code="INSURANCE", parameter="2000")
    ]

    delivery_cost = DeliveryRecipientCostRequestDto(
        value=500.0,
        vat_sum=83.33,
        vat_rate=20
    )

    result = await live_client.order.post_orders(
        type=1,  # интернет-магазин
        tariff_code=1,  # Экспресс лайт дверь-дверь
        number=f"TEST-FULL-{int(time.time())}",
        comment="Тестовый заказ с полными данными",
        sender=sender,
        recipient=recipient,
        from_location=from_location,
        to_location=to_location,
        packages=[package],
        services=services,
        delivery_recipient_cost=delivery_cost,
    )
    cdek_response_printer("order/post_full", result)

    assert isinstance(result, PostOrdersResponse)
    assert result.requests is not None
    assert len(result.requests) > 0


@pytest.mark.asyncio
async def test_post_orders_with_multiple_packages(live_client, cdek_response_printer):
    """Test creating order with multiple packages"""
    import time

    recipient = RecipientContactDto(
        name="Тестовый Получатель",
        phones=[PhoneDto(number="+79003333333")]
    )

    packages = []
    for i in range(1, 3):
        item = ItemRequestDto(
            name=f"Товар {i}",
            ware_key=f"TEST-{i:03d}",
            payment=MoneyDto(value=1000.0 * i),
            weight=500 * i,
            amount=1,
            cost=1000.0 * i
        )

        package = PackageRequestDto(
            number=str(i),
            weight=500 * i,
            items=[item]
        )
        packages.append(package)

    from_location = RequestFromLocationDto(
        code=44,
        address="ул. Тестовая, д. 10"
    )

    to_location = RequestToLocationDto(
        code=137,
        address="ул. Тестовая, д. 20"
    )

    result = await live_client.order.post_orders(
        tariff_code=1,
        recipient=recipient,
        packages=packages,
        from_location=from_location,
        to_location=to_location,
        number=f"TEST-MULTI-{int(time.time())}",
    )
    cdek_response_printer("order/post_multiple_packages", result)

    assert isinstance(result, PostOrdersResponse)
    assert result.requests is not None
    assert len(result.requests) > 0


@pytest.mark.asyncio
async def test_post_orders_door_to_door(live_client, cdek_response_printer):
    """Test creating door-to-door delivery order"""
    import time

    recipient = RecipientContactDto(
        name="Получатель Курьер",
        phones=[PhoneDto(number="+79004444444")]
    )

    from_location = RequestFromLocationDto(
        code=44,
        address="г. Москва, ул. Ленина, д. 1, кв. 1"
    )

    to_location = RequestToLocationDto(
        code=137,
        address="г. Санкт-Петербург, ул. Невский проспект, д. 1, кв. 1"
    )

    item = ItemRequestDto(
        name="Документы",
        ware_key="DOC-001",
        payment=MoneyDto(value=0.0),
        weight=100,
        amount=1,
        cost=0.0
    )

    package = PackageRequestDto(
        number="1",
        weight=100,
        items=[item]
    )

    result = await live_client.order.post_orders(
        tariff_code=1,  # Экспресс лайт дверь-дверь
        recipient=recipient,
        packages=[package],
        from_location=from_location,
        to_location=to_location,
        number=f"TEST-DOOR-{int(time.time())}",
    )
    cdek_response_printer("order/post_door_to_door", result)

    assert isinstance(result, PostOrdersResponse)
    assert result.requests is not None
    assert len(result.requests) > 0
