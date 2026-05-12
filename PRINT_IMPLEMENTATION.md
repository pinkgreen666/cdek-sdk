# Реализация методов Print Service для формирования квитанций

## Выполненная работа

### 1. Созданы модели данных (`cdek/models/print.py`)

- `PrintOrderDto` - DTO для заказа при формировании квитанции
- `PrintOrdersRequest` - Запрос на формирование квитанции
- `PrintOrdersResponse` - Ответ при создании квитанции
- `GetWaybillResponse` - Ответ при получении информации о квитанции
- `WaybillDto` - Информация о квитанции
- `WaybillStatusDto` - Статус квитанции
- Вспомогательные модели: `ErrorDto`, `WarningDto`, `RequestDto`, `RelatedEntityDto`

### 2. Реализованы методы в Print Service (`cdek/services/print.py`)

#### `post_print_orders` - Формирование квитанции
- Создает запрос на формирование квитанции в PDF
- Поддерживает до 100 заказов в одном запросе
- Параметры:
  - `orders: list[PrintOrderDto]` - список заказов
  - `copy_count: int = 2` - количество копий на листе
  - `type: str | None` - шаблон квитанции (tpl_russia, tpl_english, tpl_china и др.)
- Возвращает `PrintOrdersResponse` с UUID квитанции

#### `get_print_orders_uuid` - Получение информации о квитанции
- Получает статус формирования квитанции
- Возвращает ссылку на PDF (действительна 1 час)
- Статусы: ACCEPTED, PROCESSING, READY, INVALID, REMOVED
- Возвращает `GetWaybillResponse`

#### `get_print_orders_uuidpdf` - Скачивание PDF квитанции
- Скачивает готовую квитанцию с авторизацией
- Автоматически добавляет Bearer token
- Возвращает `bytes` - содержимое PDF файла
- **Важно**: Ссылка из `get_print_orders_uuid` не работает без авторизации, используйте этот метод для скачивания

### 3. Написаны тесты (`tests/test_print.py`)

Все тесты успешно проходят:

- ✅ `test_create_waybill_for_order` - Создание квитанции для одного заказа
- ✅ `test_get_waybill_by_uuid` - Получение информации о квитанции
- ✅ `test_create_waybill_multiple_orders` - Создание квитанции для нескольких заказов
- ✅ `test_create_waybill_with_different_templates` - Тестирование различных шаблонов
- ✅ `test_download_waybill_pdf` - Скачивание PDF файла

### 4. Создана документация

- `PRINT_SERVICE.md` - Полная документация по Print Service
- `examples/print_waybill.py` - Примеры использования всех методов
- `examples/download_waybill.py` - Пример скачивания PDF в файл

### 5. Проверка работоспособности

✅ PDF квитанция успешно скачана и сохранена:
- Файл: `waybill_example.pdf`
- Размер: 93 KB (94,517 байт)
- Формат: PDF 1.4, 1 страница
- Расположение: `/home/student/Documents/cdek-sdk/waybill_example.pdf`

## Использование

### Базовый пример

```python
from cdek import CdekClient
from cdek.models.print import PrintOrderDto

client = CdekClient(client_id="...", client_secret="...", test_mode=True)

try:
    # 1. Создаем квитанцию
    print_order = PrintOrderDto(order_uuid="order-uuid")
    waybill = await client.print.post_print_orders(
        orders=[print_order],
        copy_count=2,
        type="tpl_russia"
    )
    
    waybill_uuid = waybill.entity.uuid
    
    # 2. Ждем формирования (обычно 5-10 секунд)
    await asyncio.sleep(10)
    
    # 3. Проверяем статус
    info = await client.print.get_print_orders_uuid(waybill_uuid)
    
    if info.entity.statuses[-1].code == "READY":
        # 4. Скачиваем PDF
        pdf_content = await client.print.get_print_orders_uuidpdf(waybill_uuid)
        
        # 5. Сохраняем в файл
        with open("waybill.pdf", "wb") as f:
            f.write(pdf_content)
        
        print(f"PDF скачан: {len(pdf_content)} байт")
finally:
    await client.close()
```

### Доступные шаблоны квитанций

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

## Важные замечания

1. **Авторизация для скачивания**: Ссылка из `get_print_orders_uuid` требует Bearer token. Используйте метод `get_print_orders_uuidpdf` для скачивания PDF.

2. **Время жизни ссылки**: Ссылка на PDF действительна только 1 час после формирования.

3. **Лимиты**: Максимум 100 заказов в одном запросе на формирование квитанции.

4. **Статусы**: Проверяйте статус `READY` перед скачиванием PDF.

5. **Копии**: Рекомендуется указывать `copy_count` не менее 2 (одна копия для груза, вторая для отправителя).

## Запуск тестов

```bash
# Все тесты print сервиса
pytest tests/test_print.py -v

# Конкретный тест
pytest tests/test_print.py::test_download_waybill_pdf -v -s
```

## Файлы

- `cdek/models/print.py` - Модели данных
- `cdek/services/print.py` - Реализация сервиса
- `tests/test_print.py` - Тесты
- `examples/print_waybill.py` - Примеры использования
- `examples/download_waybill.py` - Пример скачивания
- `PRINT_SERVICE.md` - Документация
- `waybill_example.pdf` - Пример скачанной квитанции
