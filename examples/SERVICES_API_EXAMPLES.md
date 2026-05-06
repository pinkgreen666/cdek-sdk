# Примеры использования API дополнительных услуг CDEK

## Запуск сервера

```bash
# Установите переменные окружения
export CDEK_CLIENT_ID="your_client_id"
export CDEK_CLIENT_SECRET="your_client_secret"

# Запустите сервер
python examples/fastapi_services_guide.py
```

Сервер будет доступен на `http://localhost:8000`

Документация API: `http://localhost:8000/docs`

---

## 1. Получить все доступные услуги

### Все услуги
```bash
curl http://localhost:8000/services
```

### Только для доставки до двери
```bash
curl "http://localhost:8000/services?mode=warehouse-door"
```

### Только для посылок до 5 кг
```bash
curl "http://localhost:8000/services?max_weight=5"
```

### Только услуги, требующие параметр
```bash
curl "http://localhost:8000/services?requires_parameter=true"
```

**Ответ:**
```json
[
  {
    "code": "SMS",
    "name": "Уведомление о вручении заказа",
    "description": "СМС-уведомление отправителю с датой и временем доставки...",
    "modes": null,
    "weight_limit": null,
    "requires_parameter": false,
    "auto_added": false,
    "restrictions": null
  },
  {
    "code": "INSURANCE",
    "name": "Страхование",
    "description": "Обеспечение страховой защиты посылки...",
    "modes": null,
    "weight_limit": null,
    "requires_parameter": true,
    "auto_added": true,
    "restrictions": "Для ИМ добавляется автоматически"
  }
]
```

---

## 2. Получить информацию о конкретной услуге

```bash
curl http://localhost:8000/services/INSURANCE
```

**Ответ:**
```json
{
  "code": "INSURANCE",
  "name": "Страхование",
  "description": "Обеспечение страховой защиты посылки...",
  "modes": null,
  "weight_limit": null,
  "requires_parameter": true,
  "auto_added": true,
  "restrictions": "Для ИМ добавляется автоматически"
}
```

---

## 3. Получить услуги с параметрами

```bash
curl http://localhost:8000/services-with-parameters
```

**Ответ:**
```json
[
  {
    "code": "INSURANCE",
    "name": "Страхование",
    "requires_parameter": true
  },
  {
    "code": "GET_UP_FLOOR_BY_HAND",
    "name": "Подъём на этаж (по лестнице)",
    "requires_parameter": true
  }
]
```

---

## 4. Рассчитать стоимость с услугами

### Пример 1: Услуги БЕЗ параметров

```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "tariff_code": 136,
    "from_location": 270,
    "to_location": 44,
    "weight": 1000,
    "length": 30,
    "width": 20,
    "height": 10,
    "services": [
      {"code": "SMS"},
      {"code": "TRYING_ON"}
    ]
  }'
```

### Пример 2: Услуги С параметрами

```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "tariff_code": 136,
    "from_location": 270,
    "to_location": 44,
    "weight": 15000,
    "length": 40,
    "width": 30,
    "height": 20,
    "services": [
      {"code": "SMS"},
      {"code": "GET_UP_FLOOR_BY_HAND", "parameter": 5}
    ]
  }'
```

### Пример 3: Смешанные услуги

```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "tariff_code": 136,
    "from_location": 270,
    "to_location": 44,
    "weight": 2000,
    "length": 30,
    "width": 20,
    "height": 15,
    "services": [
      {"code": "SMS"},
      {"code": "TRYING_ON"},
      {"code": "PART_DELIV"},
      {"code": "GET_UP_FLOOR_BY_HAND", "parameter": 3}
    ]
  }'
```

**Ответ:**
```json
{
  "success": true,
  "calculation": {
    "total_sum": 450.5,
    "delivery_sum": 350.0,
    "period_min": 2,
    "period_max": 4,
    "currency": "RUB"
  },
  "services_applied": [
    {
      "code": "SMS",
      "name": "Уведомление о вручении заказа",
      "parameter": null
    },
    {
      "code": "GET_UP_FLOOR_BY_HAND",
      "name": "Подъём на этаж (по лестнице)",
      "parameter": 3
    }
  ]
}
```

---

## 5. Руководство по использованию

```bash
curl http://localhost:8000/services/guide
```

**Ответ:**
```json
{
  "guide": {
    "simple_services": {
      "description": "Услуги без параметров - просто указываете код",
      "examples": [
        {"code": "SMS", "name": "Уведомление о вручении"},
        {"code": "TRYING_ON", "name": "Примерка"}
      ],
      "usage": {"code": "SMS"}
    },
    "parametrized_services": {
      "description": "Услуги с параметрами - нужно указать значение",
      "examples": [
        {
          "code": "GET_UP_FLOOR_BY_HAND",
          "name": "Подъём на этаж",
          "parameter_description": "Количество этажей (число)"
        }
      ],
      "usage": {
        "code": "GET_UP_FLOOR_BY_HAND",
        "parameter": 5
      }
    }
  }
}
```

---

## Ключевые моменты

### 1. Услуги БЕЗ параметров
Просто указываешь код:
```json
{"code": "SMS"}
{"code": "TRYING_ON"}
{"code": "PART_DELIV"}
```

### 2. Услуги С параметрами
Указываешь код + значение параметра:
```json
{"code": "GET_UP_FLOOR_BY_HAND", "parameter": 5}
{"code": "INSURANCE", "parameter": 5000}
```

### 3. Автоматические услуги
`INSURANCE` для интернет-магазинов добавляется автоматически - не нужно передавать в `services`.

### 4. Ограничения по режиму доставки
Некоторые услуги доступны только для определенных режимов:
- `THERMAL_MODE` - только `warehouse-warehouse`
- `DELIV_RECEIVER` - только `warehouse-warehouse`

### 5. Ограничения по весу
`GET_UP_FLOOR_BY_HAND` - только для посылок от 10 кг до 150 кг.

---

## Типичные ошибки

### Ошибка: Не указан параметр для услуги
```json
{
  "detail": "Услуга 'Подъём на этаж (по лестнице)' (GET_UP_FLOOR_BY_HAND) требует параметр"
}
```
**Решение:** Добавь `"parameter": 5` к услуге.

### Ошибка: Указан параметр для услуги, которая его не требует
```json
{
  "detail": "Услуга 'Уведомление о вручении заказа' (SMS) не требует параметр"
}
```
**Решение:** Убери `parameter` из объекта услуги.

### Ошибка: Услуга не найдена
```json
{
  "detail": "Услуга 'INVALID_CODE' не найдена"
}
```
**Решение:** Проверь код услуги через `/services`.

---

## Python клиент

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Получить все услуги
        response = await client.get("http://localhost:8000/services")
        services = response.json()
        print(f"Всего услуг: {len(services)}")
        
        # Рассчитать с услугами
        response = await client.post(
            "http://localhost:8000/calculate",
            json={
                "tariff_code": 136,
                "from_location": 270,
                "to_location": 44,
                "weight": 1000,
                "length": 30,
                "width": 20,
                "height": 10,
                "services": [
                    {"code": "SMS"},
                    {"code": "TRYING_ON"}
                ]
            }
        )
        result = response.json()
        print(f"Стоимость: {result['calculation']['total_sum']} RUB")

asyncio.run(main())
```

---

## JavaScript/TypeScript клиент

```typescript
// Получить все услуги
const services = await fetch('http://localhost:8000/services')
  .then(r => r.json());

console.log(`Всего услуг: ${services.length}`);

// Рассчитать с услугами
const result = await fetch('http://localhost:8000/calculate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    tariff_code: 136,
    from_location: 270,
    to_location: 44,
    weight: 1000,
    length: 30,
    width: 20,
    height: 10,
    services: [
      {code: 'SMS'},
      {code: 'TRYING_ON'}
    ]
  })
}).then(r => r.json());

console.log(`Стоимость: ${result.calculation.total_sum} RUB`);
```
