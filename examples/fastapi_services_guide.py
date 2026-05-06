"""
Полное руководство по работе с дополнительными услугами CDEK через FastAPI.

Этот пример показывает:
1. Как получить список всех доступных услуг
2. Как фильтровать услуги по режиму доставки и весу
3. Как определить какие услуги требуют параметры
4. Как правильно передавать параметры для услуг
"""
import os
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from cdek import CdekClient
from cdek.reference import get_service, list_services


app = FastAPI(title="CDEK Services API Guide")


# === Response Models ===

class ServiceDetail(BaseModel):
    """Детальная информация об услуге."""
    code: str
    name: str
    description: str
    modes: Optional[List[str]] = Field(
        None,
        description="Режимы доставки: warehouse-warehouse, warehouse-door, warehouse-postamat"
    )
    weight_limit: Optional[float] = Field(
        None,
        description="Максимальный вес для услуги (кг)"
    )
    requires_parameter: bool = Field(
        False,
        description="Требуется ли параметр при добавлении услуги"
    )
    auto_added: bool = Field(
        False,
        description="Добавляется ли услуга автоматически (например, страхование для ИМ)"
    )
    restrictions: Optional[str] = Field(
        None,
        description="Ограничения и особенности использования"
    )


class ServiceParameter(BaseModel):
    """Параметр для услуги."""
    code: str = Field(..., description="Код услуги")
    parameter: Optional[float] = Field(
        None,
        description="Значение параметра (например, количество этажей или сумма страхования)"
    )


class CalculateRequest(BaseModel):
    """Запрос на расчет стоимости с услугами."""
    tariff_code: int = Field(..., description="Код тарифа CDEK")
    from_location: int = Field(..., description="Код города отправителя")
    to_location: int = Field(..., description="Код города получателя")
    weight: float = Field(..., description="Вес посылки в граммах")
    length: float = Field(..., description="Длина в см")
    width: float = Field(..., description="Ширина в см")
    height: float = Field(..., description="Высота в см")
    services: List[ServiceParameter] = Field(
        default_factory=list,
        description="Список дополнительных услуг с параметрами"
    )


# === Startup/Shutdown ===

@app.on_event("startup")
async def startup():
    app.state.cdek = CdekClient(
        client_id=os.getenv("CDEK_CLIENT_ID"),
        client_secret=os.getenv("CDEK_CLIENT_SECRET"),
        test_mode=True
    )


@app.on_event("shutdown")
async def shutdown():
    await app.state.cdek.close()


# === Endpoints ===

@app.get("/services", response_model=List[ServiceDetail])
async def get_all_services(
    mode: Optional[str] = Query(
        None,
        description="Фильтр по режиму доставки",
        enum=["warehouse-warehouse", "warehouse-door", "warehouse-postamat"]
    ),
    max_weight: Optional[float] = Query(
        None,
        description="Фильтр по максимальному весу (кг)"
    ),
    requires_parameter: Optional[bool] = Query(
        None,
        description="Показать только услуги, требующие параметр"
    )
):
    """
    Получить список всех доступных дополнительных услуг.

    Примеры:
    - GET /services - все услуги
    - GET /services?mode=warehouse-door - только для доставки до двери
    - GET /services?max_weight=5 - только для посылок до 5 кг
    - GET /services?requires_parameter=true - только услуги с параметрами
    """
    services = list_services(mode=mode, max_weight=max_weight)

    # Дополнительная фильтрация по requires_parameter
    if requires_parameter is not None:
        services = [s for s in services if s.requires_parameter == requires_parameter]

    return [
        ServiceDetail(
            code=s.code,
            name=s.name,
            description=s.description,
            modes=s.modes,
            weight_limit=s.weight_limit,
            requires_parameter=s.requires_parameter,
            auto_added=s.auto_added,
            restrictions=s.restrictions
        )
        for s in services
    ]


@app.get("/services/{service_code}", response_model=ServiceDetail)
async def get_service_info(service_code: str):
    """
    Получить детальную информацию о конкретной услуге.

    Пример:
    - GET /services/INSURANCE
    - GET /services/GET_UP_FLOOR_BY_HAND
    """
    service = get_service(service_code)
    if not service:
        raise HTTPException(
            status_code=404,
            detail=f"Услуга с кодом '{service_code}' не найдена"
        )

    return ServiceDetail(
        code=service.code,
        name=service.name,
        description=service.description,
        modes=service.modes,
        weight_limit=service.weight_limit,
        requires_parameter=service.requires_parameter,
        auto_added=service.auto_added,
        restrictions=service.restrictions
    )


@app.get("/services-with-parameters", response_model=List[ServiceDetail])
async def get_services_requiring_parameters():
    """
    Получить список услуг, которые требуют параметр.

    Сейчас это:
    - INSURANCE (requires_parameter=true) - требует сумму страхования
    - GET_UP_FLOOR_BY_HAND (requires_parameter=true) - требует количество этажей

    Пример:
    - GET /services-with-parameters
    """
    all_services = list_services()
    services_with_params = [s for s in all_services if s.requires_parameter]

    return [
        ServiceDetail(
            code=s.code,
            name=s.name,
            description=s.description,
            modes=s.modes,
            weight_limit=s.weight_limit,
            requires_parameter=s.requires_parameter,
            auto_added=s.auto_added,
            restrictions=s.restrictions
        )
        for s in services_with_params
    ]


@app.post("/calculate")
async def calculate_with_services(request: CalculateRequest):
    """
    Рассчитать стоимость доставки с дополнительными услугами.

    Пример запроса:
    ```json
    {
        "tariff_code": 136,
        "from_location": 270,
        "to_location": 44,
        "weight": 1000,
        "length": 30,
        "width": 20,
        "height": 10,
        "services": [
            {"code": "SMS"},
            {"code": "TRYING_ON"},
            {"code": "GET_UP_FLOOR_BY_HAND", "parameter": 5}
        ]
    }
    ```

    Важно:
    - Для услуг БЕЗ параметра: {"code": "SMS"}
    - Для услуг С параметром: {"code": "GET_UP_FLOOR_BY_HAND", "parameter": 5}
    - INSURANCE обычно добавляется автоматически для ИМ
    """
    # Валидация услуг
    validated_services = []

    for service_param in request.services:
        service = get_service(service_param.code)

        if not service:
            raise HTTPException(
                status_code=400,
                detail=f"Услуга '{service_param.code}' не найдена"
            )

        # Проверка параметра
        if service.requires_parameter and service_param.parameter is None:
            raise HTTPException(
                status_code=400,
                detail=f"Услуга '{service.name}' ({service_param.code}) требует параметр. "
                       f"Описание: {service.description}"
            )

        if not service.requires_parameter and service_param.parameter is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Услуга '{service.name}' ({service_param.code}) не требует параметр"
            )

        # Формируем объект для API
        service_obj = {"code": service_param.code}
        if service_param.parameter is not None:
            service_obj["parameter"] = service_param.parameter

        validated_services.append(service_obj)

    # Вызов API CDEK
    try:
        result = await app.state.cdek.calculator.calculate_tariff(
            tariff_code=request.tariff_code,
            from_location=request.from_location,
            to_location=request.to_location,
            packages=[{
                "weight": request.weight,
                "length": request.length,
                "width": request.width,
                "height": request.height
            }],
            services=validated_services
        )

        return {
            "success": True,
            "calculation": {
                "total_sum": result.total_sum,
                "delivery_sum": result.delivery_sum,
                "period_min": result.period_min,
                "period_max": result.period_max,
                "currency": result.currency
            },
            "services_applied": [
                {
                    "code": sp.code,
                    "name": get_service(sp.code).name,
                    "parameter": sp.parameter
                }
                for sp in request.services
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при расчете: {str(e)}"
        )


@app.get("/services/guide")
async def services_usage_guide():
    """
    Руководство по использованию услуг.

    Возвращает примеры использования разных типов услуг.
    """
    return {
        "guide": {
            "simple_services": {
                "description": "Услуги без параметров - просто указываете код",
                "examples": [
                    {"code": "SMS", "name": "Уведомление о вручении"},
                    {"code": "TRYING_ON", "name": "Примерка"},
                    {"code": "PART_DELIV", "name": "Частичная доставка"}
                ],
                "usage": {
                    "code": "SMS"
                }
            },
            "parametrized_services": {
                "description": "Услуги с параметрами - нужно указать значение",
                "examples": [
                    {
                        "code": "GET_UP_FLOOR_BY_HAND",
                        "name": "Подъём на этаж",
                        "parameter_description": "Количество этажей (число)"
                    },
                    {
                        "code": "INSURANCE",
                        "name": "Страхование",
                        "parameter_description": "Сумма страхования (рубли)",
                        "note": "Для ИМ добавляется автоматически"
                    }
                ],
                "usage": {
                    "code": "GET_UP_FLOOR_BY_HAND",
                    "parameter": 5
                }
            },
            "auto_added_services": {
                "description": "Услуги, которые добавляются автоматически",
                "examples": [
                    {
                        "code": "INSURANCE",
                        "name": "Страхование",
                        "note": "Для заказов типа 'Интернет-магазин' добавляется автоматически"
                    }
                ]
            },
            "mode_restricted_services": {
                "description": "Услуги доступны только для определенных режимов доставки",
                "examples": [
                    {
                        "code": "THERMAL_MODE",
                        "name": "Тепловой режим",
                        "modes": ["warehouse-warehouse"]
                    },
                    {
                        "code": "DELIV_RECEIVER",
                        "name": "Доставка в городе получателе",
                        "modes": ["warehouse-warehouse"]
                    }
                ]
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
