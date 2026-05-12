# Получение информации о заказах CDEK

## Важно: API не поддерживает получение всех заказов

CDEK API **НЕ** позволяет получить список всех ваших заказов без фильтра. Вы **ОБЯЗАНЫ** указать один из параметров:
- `cdek_number` - номер заказа в системе CDEK
- `im_number` - ваш внутренний номер заказа (рекомендуется)
- `uuid` - UUID заказа

## Рекомендуемый подход

### 1. При создании заказа всегда указывайте ваш внутренний номер

```python
from cdek import CdekClient

async with CdekClient(client_id="...", client_secret="...", test_mode=True) as client:
    # Используйте ваш внутренний ID заказа из вашей базы данных
    your_order_id = "ORDER-12345"
    
    result = await client.order.post_orders(
        number=your_order_id,  # ВАШ внутренний номер заказа
        tariff_code=136,
        recipient=recipient,
        packages=[package],
        shipment_point="MSK1",
        delivery_point="SPB1",
    )
    
    # Сохраните UUID для дополнительного доступа
    uuid = result.entity.uuid
```

### 2. Получение заказа по вашему внутреннему номеру (IM number)

```python
# Самый надёжный способ - вы контролируете этот номер
order = await client.order.get_orders(im_number="ORDER-12345")

print(f"Статус: {order.entity.statuses[-1].name}")
print(f"CDEK номер: {order.entity.cdek_number}")
```

### 3. Получение заказа по UUID

```python
# Если вы сохранили UUID при создании
order = await client.order.get_orders_uuid("uuid-заказа")

print(f"Номер заказа: {order.entity.number}")
print(f"CDEK номер: {order.entity.cdek_number}")
```

### 4. Получение заказа по CDEK номеру

```python
# Если вы сохранили CDEK номер из предыдущего запроса
order = await client.order.get_orders(cdek_number=1107205518)

print(f"Ваш номер: {order.entity.number}")
```

## Что нужно сохранять в вашей базе данных

При создании заказа сохраните:

```python
{
    "your_order_id": "ORDER-12345",           # Ваш ID (обязательно!)
    "cdek_uuid": "ec832d39-f308-42c6-...",    # UUID от CDEK
    "cdek_number": "1107205518",              # Номер CDEK (после обработки)
    "created_at": "2026-05-12T07:00:00Z"
}
```

## Примеры тестов

См. `tests/test_order.py`:
- `test_create_and_get_order_by_uuid` - создание и получение по UUID с сохранением в файл
- `test_get_order_by_im_number_after_creation` - создание и получение по IM номеру

## Методы SDK

```python
# Получение по CDEK номеру или IM номеру
order = await client.order.get_orders(
    cdek_number=1107205518,  # опционально
    im_number="ORDER-12345"  # опционально
)

# Получение по UUID
order = await client.order.get_orders_uuid("uuid-заказа")
```

## Структура ответа

```python
GetOrdersResponse(
    entity=OrderResponseDto(
        uuid="...",
        cdek_number="1107205518",
        number="ORDER-12345",  # ваш внутренний номер
        recipient=RecipientResponseContactDto(...),
        packages=[...],
        statuses=[
            OrderStatusDto(code="CREATED", name="Создан", ...),
            OrderStatusDto(code="ACCEPTED", name="Принят", ...)
        ],
        ...
    ),
    requests=[...],
    related_entities=[...]
)
```
