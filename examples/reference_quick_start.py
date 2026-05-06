"""
Example: Quick reference data usage

This example shows the most common use cases for CDEK reference data.
"""

import asyncio
import os
from cdek import CdekClient
from cdek.reference import get_service, suggest_box, list_services, get_packaging_services
from cdek.models.calculator import (
    CalculatorLocationDto,
    CalcPackageRequestDto,
    CalcAdditionalServiceDto,
)


async def main():
    # Example 1: Get service information
    print("=== Service Information ===")
    insurance = get_service("INSURANCE")
    if insurance:
        print(f"Service: {insurance.name}")
        print(f"Description: {insurance.description}")
        print(f"Auto-added: {insurance.auto_added}")
        print(f"Requires parameter: {insurance.requires_parameter}")
    print()

    # Example 2: Find suitable packaging
    print("=== Packaging Suggestion ===")
    weight = 3.5  # kg
    mode = "warehouse-door"
    box = suggest_box(weight, mode)
    if box:
        print(f"For {weight}kg package:")
        print(f"  Recommended: {box.name}")
        print(f"  Dimensions: {box.dimensions}")
        print(f"  Max weight: {box.max_weight} kg")
    else:
        print(f"No suitable box found for {weight}kg")
    print()

    # Example 3: List all packaging options
    print("=== All Packaging Options ===")
    packages = get_packaging_services()
    for pkg in packages[:5]:  # Show first 5
        print(f"• {pkg.name} (code: {pkg.code})")
        if pkg.max_weight:
            print(f"  Max weight: {pkg.max_weight} kg")
        if pkg.dimensions:
            print(f"  Dimensions: {pkg.dimensions}")
    print(f"... and {len(packages) - 5} more")
    print()

    # Example 4: List services by mode
    print("=== Services for warehouse-door mode ===")
    services = list_services(mode="warehouse-door")
    for service in services[:5]:  # Show first 5
        print(f"✓ {service.name} ({service.code})")
        if service.restrictions:
            print(f"  ⚠️  {service.restrictions}")
    print()

    # Example 5: Combine with API call
    print("=== Calculate with Services ===")

    # Get credentials from environment
    client_id = os.getenv("CDEK_CLIENT_ID", "your_client_id")
    client_secret = os.getenv("CDEK_CLIENT_SECRET", "your_client_secret")

    if client_id == "your_client_id":
        print("⚠️  Set CDEK_CLIENT_ID and CDEK_CLIENT_SECRET environment variables to run API example")
        return

    client = CdekClient(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True
    )

    try:
        # Validate service before using
        sms_service = get_service("SMS")
        if sms_service:
            print(f"Using service: {sms_service.name}")
            if sms_service.restrictions:
                print(f"Restrictions: {sms_service.restrictions}")

        # Calculate tariff with services
        result = await client.calculator.post_calculator_tariff(
            tariff_code=136,
            from_location=CalculatorLocationDto(code=270),  # Moscow
            to_location=CalculatorLocationDto(code=44),  # Saint Petersburg
            packages=[
                CalcPackageRequestDto(
                    weight=1000,  # grams
                    length=30,
                    width=20,
                    height=10,
                )
            ],
            services=[CalcAdditionalServiceDto(code="SMS")],
        )

        print(f"Total cost: {result.total_sum} {result.currency}")
        print(f"Delivery: {result.period_min}-{result.period_max} days")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
