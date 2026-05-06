"""
Example: Using CDEK reference data in FastAPI application.

This example shows how to use CDEK SDK reference data to build
a delivery service selection UI for an e-commerce application.
"""
import os
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from cdek import CdekClient
from cdek.reference import (
    get_service,
    list_services,
    get_packaging_services,
    suggest_box,
)


app = FastAPI(title="CDEK Delivery API")


# Response models for API
class ServiceInfo(BaseModel):
    code: str
    name: str
    description: str
    modes: Optional[List[str]] = None
    weight_limit: Optional[float] = None
    requires_parameter: bool = False
    restrictions: Optional[str] = None


class BoxSuggestion(BaseModel):
    code: str
    name: str
    dimensions: Optional[str] = None
    max_weight: Optional[float] = None
    description: str


# Initialize CDEK client on startup
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


@app.get("/api/services", response_model=List[ServiceInfo])
async def get_available_services(
    mode: Optional[str] = Query(None, description="Delivery mode filter"),
    max_weight: Optional[float] = Query(None, description="Maximum weight filter")
):
    """Get list of available additional services with optional filters.

    Example:
        GET /api/services?mode=warehouse-door&max_weight=10
    """
    services = list_services(mode=mode, max_weight=max_weight)
    return [
        ServiceInfo(
            code=s.code,
            name=s.name,
            description=s.description,
            modes=s.modes,
            weight_limit=s.weight_limit,
            requires_parameter=s.requires_parameter,
            restrictions=s.restrictions
        )
        for s in services
    ]


@app.get("/api/services/{service_code}", response_model=ServiceInfo)
async def get_service_details(service_code: str):
    """Get details about a specific service.

    Example:
        GET /api/services/INSURANCE
    """
    service = get_service(service_code)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return ServiceInfo(
        code=service.code,
        name=service.name,
        description=service.description,
        modes=service.modes,
        weight_limit=service.weight_limit,
        requires_parameter=service.requires_parameter,
        restrictions=service.restrictions
    )


@app.get("/api/packaging", response_model=List[ServiceInfo])
async def get_packaging_options():
    """Get all available packaging options (boxes, envelopes, etc.).

    Example:
        GET /api/packaging
    """
    services = get_packaging_services()
    return [
        ServiceInfo(
            code=s.code,
            name=s.name,
            description=s.description,
            modes=s.modes,
            weight_limit=s.max_weight
        )
        for s in services
    ]


@app.get("/api/packaging/suggest", response_model=BoxSuggestion)
async def suggest_packaging(
    weight: float = Query(..., description="Package weight in kg"),
    mode: str = Query("warehouse-door", description="Delivery mode")
):
    """Suggest appropriate packaging based on weight and delivery mode.

    Example:
        GET /api/packaging/suggest?weight=3.5&mode=warehouse-door
    """
    box = suggest_box(weight, mode)
    if not box:
        raise HTTPException(
            status_code=404,
            detail=f"No suitable packaging found for {weight}kg with mode {mode}"
        )

    return BoxSuggestion(
        code=box.code,
        name=box.name,
        dimensions=box.dimensions,
        max_weight=box.max_weight,
        description=box.description
    )


@app.post("/api/calculate-with-services")
async def calculate_delivery_with_services(
    tariff_code: int,
    from_location: int,
    to_location: int,
    weight: float,
    length: float,
    width: float,
    height: float,
    service_codes: List[str] = []
):
    """Calculate delivery cost with selected additional services.

    This endpoint combines CDEK API tariff calculation with reference data
    to provide full service information.

    Example:
        POST /api/calculate-with-services
        {
            "tariff_code": 136,
            "from_location": 270,
            "to_location": 44,
            "weight": 1000,
            "length": 30,
            "width": 20,
            "height": 10,
            "service_codes": ["INSURANCE", "SMS"]
        }
    """
    # Validate service codes
    invalid_services = []
    services_info = []

    for code in service_codes:
        service = get_service(code)
        if not service:
            invalid_services.append(code)
        else:
            services_info.append({
                "code": service.code,
                "name": service.name,
                "auto_added": service.auto_added,
                "requires_parameter": service.requires_parameter
            })

    if invalid_services:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service codes: {', '.join(invalid_services)}"
        )

    # Calculate tariff using CDEK API
    try:
        result = await app.state.cdek.calculator.calculate_tariff(
            tariff_code=tariff_code,
            from_location=from_location,
            to_location=to_location,
            packages=[{
                "weight": weight,
                "length": length,
                "width": width,
                "height": height
            }],
            services=[{"code": code} for code in service_codes]
        )

        return {
            "calculation": {
                "total_sum": result.total_sum,
                "delivery_sum": result.delivery_sum,
                "period_min": result.period_min,
                "period_max": result.period_max,
                "currency": result.currency
            },
            "services": services_info,
            "suggested_box": None if weight > 30 else suggest_box(weight / 1000, "warehouse-door")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Frontend helper endpoint
@app.get("/api/delivery-wizard")
async def delivery_wizard(
    weight: float = Query(..., description="Package weight in kg"),
    mode: str = Query("warehouse-door", description="Delivery mode"),
    is_ecommerce: bool = Query(False, description="Is this for e-commerce order")
):
    """Get recommended configuration for delivery (box + services).

    This is a helper endpoint that combines multiple reference lookups
    to provide a complete delivery configuration recommendation.

    Example:
        GET /api/delivery-wizard?weight=2.5&mode=warehouse-door&is_ecommerce=true
    """
    # Suggest packaging
    box = suggest_box(weight, mode)

    # Get recommended services based on context
    recommended_services = []

    if is_ecommerce:
        # For e-commerce, recommend common services
        recommended_codes = ["INSURANCE", "SMS", "TRYING_ON", "PART_DELIV"]
        for code in recommended_codes:
            service = get_service(code)
            if service and (service.modes is None or mode in service.modes):
                recommended_services.append({
                    "code": service.code,
                    "name": service.name,
                    "description": service.description,
                    "restrictions": service.restrictions
                })

    return {
        "suggested_box": {
            "code": box.code,
            "name": box.name,
            "dimensions": box.dimensions,
            "max_weight": box.max_weight
        } if box else None,
        "recommended_services": recommended_services,
        "all_available_services": [
            {"code": s.code, "name": s.name}
            for s in list_services(mode=mode, max_weight=weight)
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
