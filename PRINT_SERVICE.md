# Print Service - Формирование квитанций к заказам

## Обзор

Print Service предоставляет методы для формирования и получения квитанций (waybill) к заказам в формате PDF.

## Реализованные методы

### 1. `post_print_orders` - Формирование квитанции

Создает запрос на формирование квитанции в формате PDF для одного или нескольких заказов.

**Параметры:**
- `orders: list[PrintOrderDto]` - Список заказов (максимум 100)
- `copy_count: int = 2` - Число копий одной квитанции на листе (рекомендуется минимум 2)
- `type: str | None` - Форма квитанции (шаблон)

**Доступные шаблоны:**
- `tpl_russia` - Русский (по умолчанию)
- `tpl_english` - Английский
- `tpl_china` - Китайский
- `tpl_armenia` - Армянский
- `tpl_italian` - Итальянский
- `tpl_korean` - Корейский
- `tpl_latvian` - Латышский
- `tpl_lithuanian` - Литовский
- `tpl_german` - Немецкий
- `tpl_turkish` - Турецкий
- `tpl_czech` - Чешский
- `tpl_thailand` - Тайский
- `tpl_invoice` - Инвойс

**Возвращает:** `PrintOrdersResponse` с UUID запроса

**Пример:**
```python
from cdek.models.print import PrintOrderDto

print_order = PrintOrderDto(order_uuid="order-uuid-here")

waybill = await client.print.post_print_orders(
    orders=[print_order],
    copy_count=2,
    type="tpl_russia"
)

print(f"Waybill UUID: {waybill.entity.uuid}")
```

### 2. `get_print_orders_uuid` - Получение квитанции

Получает информацию о квитанции, включая ссылку на скачивание PDF (если квитанция готова).

**Параметры:**
- `uuid: str` - UUID запроса на формирование квитанции

**Возвращает:** `GetWaybillResponse` со ссылкой на PDF и статусами

**Статусы квитанции:**
- `ACCEPTED` - Запрос принят
- `INVALID` - Некорректный запрос
- `PROCESSING` - Файл формируется
- `READY` - Файл сформирован, ссылка доступна
- `REMOVED` - Срок действия ссылки истек

**Важно:** Ссылка на PDF доступна в течение 1 часа после формирования.

**Пример:**
```python
waybill = await client.print.get_print_orders_uuid(waybill_uuid)

if waybill.entity.statuses:
    latest_status = waybill.entity.statuses[-1]
    
    if latest_status.code == "READY":
        print(f"Download URL: {waybill.entity.url}")
        print("Note: URL is valid for 1 hour")
    elif latest_status.code == "PROCESSING":
        print("Waybill is being generated...")
```

### 3. `get_print_orders_uuidpdf` - Скачивание PDF квитанции

Скачивает готовую квитанцию в формате PDF с авторизацией.

**Параметры:**
- `uuid: str` - UUID запроса на формирование квитанции

**Возвращает:** `bytes` - Содержимое PDF файла

**Важно:** 
- Квитанция должна быть в статусе `READY`
- Метод автоматически добавляет Bearer token для авторизации
- Ссылка из `get_print_orders_uuid` не работает без авторизации, используйте этот метод

**Пример:**
```python
# Скачиваем PDF
pdf_content = await client.print.get_print_orders_uuidpdf(waybill_uuid)

# Сохраняем в файл
with open("waybill.pdf", "wb") as f:
    f.write(pdf_content)

print(f"PDF downloaded: {len(pdf_content)} bytes")
```

## Модели данных

### PrintOrderDto
```python
class PrintOrderDto(BaseModel):
    order_uuid: str  # UUID заказа
    cdek_number: str | None = None  # Номер заказа CDEK (опционально)
```

### WaybillDto
```python
class WaybillDto(BaseModel):
    uuid: str  # UUID квитанции
    url: str | None  # Ссылка на скачивание PDF
    statuses: list[WaybillStatusDto] | None  # История статусов
```

### WaybillStatusDto
```python
class WaybillStatusDto(BaseModel):
    code: str  # Код статуса (ACCEPTED, PROCESSING, READY, etc.)
    name: str | None  # Название статуса
    date_time: str | None  # Дата и время установки статуса
```

## Примеры использования

### Создание квитанции для одного заказа

```python
from cdek import CdekClient
from cdek.models.print import PrintOrderDto

async with CdekClient(client_id="...", client_secret="...", test_mode=True) as client:
    # Создаем квитанцию
    print_order = PrintOrderDto(order_uuid="order-uuid")
    
    waybill = await client.print.post_print_orders(
        orders=[print_order],
        copy_count=2,
        type="tpl_russia"
    )
    
    waybill_uuid = waybill.entity.uuid
    
    # Ждем формирования
    await asyncio.sleep(10)
    
    # Получаем ссылку
    result = await client.print.get_print_orders_uuid(waybill_uuid)
    
    if result.entity.url:
        print(f"Download: {result.entity.url}")
```

### Создание квитанции для нескольких заказов

```python
# Можно создать одну квитанцию для нескольких заказов (до 100)
print_orders = [
    PrintOrderDto(order_uuid="uuid-1"),
    PrintOrderDto(order_uuid="uuid-2"),
    PrintOrderDto(order_uuid="uuid-3"),
]

waybill = await client.print.post_print_orders(
    orders=print_orders,
    copy_count=2
)
```

### Проверка статуса с опросом

```python
async def wait_for_waybill(client, waybill_uuid, max_attempts=10):
    for attempt in range(max_attempts):
        waybill = await client.print.get_print_orders_uuid(waybill_uuid)
        
        if waybill.entity.statuses:
            latest = waybill.entity.statuses[-1]
            
            if latest.code == "READY":
                return waybill.entity.url
            elif latest.code == "INVALID":
                raise Exception("Invalid waybill request")
        
        await asyncio.sleep(3)
    
    raise TimeoutError("Waybill generation timeout")
```

## Ограничения

- Максимум 100 заказов в одном запросе
- Ссылка на PDF действительна 1 час
- Рекомендуется указывать `copy_count` не менее 2 (одна копия приклеивается на груз, вторая остается у отправителя)

## Тесты

Все методы покрыты тестами в `tests/test_print.py`:

- `test_create_waybill_for_order` - Создание квитанции для одного заказа
- `test_get_waybill_by_uuid` - Получение квитанции по UUID
- `test_create_waybill_multiple_orders` - Создание квитанции для нескольких заказов
- `test_create_waybill_with_different_templates` - Тестирование различных шаблонов

Запуск тестов:
```bash
pytest tests/test_print.py -v
```

## Полные примеры

См. `examples/print_waybill.py` для подробных примеров использования всех методов.
