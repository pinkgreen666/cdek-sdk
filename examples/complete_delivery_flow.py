"""
Complete example: E-commerce delivery configuration

This example demonstrates a complete flow for an e-commerce application:
1. User enters package details
2. System suggests packaging
3. System recommends additional services
4. Calculate delivery cost with selected services
"""
import asyncio
import os
from cdek import CdekClient
from cdek.reference import get_service, suggest_box, list_services
from cdek.exceptions import CdekError


async def configure_delivery(
    weight_kg: float,
    from_city_code: int,
    to_city_code: int,
    tariff_code: int = 136,  # Warehouse-warehouse
    is_ecommerce: bool = True
):
    """
    Complete delivery configuration flow.

    Args:
        weight_kg: Package weight in kilograms
        from_city_code: Sender city code
        to_city_code: Recipient city code
        tariff_code: CDEK tariff code
        is_ecommerce: Whether this is an e-commerce order
    """
    print("=" * 60)
    print("CDEK Delivery Configuration")
    print("=" * 60)

    # Step 1: Suggest packaging
    print(f"\n📦 Package weight: {weight_kg} kg")
    box = suggest_box(weight_kg, "warehouse-warehouse")

    if box:
        print(f"\n✓ Recommended packaging:")
        print(f"  {box.name}")
        print(f"  Dimensions: {box.dimensions} cm")
        print(f"  Max weight: {box.max_weight} kg")
        print(f"  Code: {box.code}")
    else:
        print(f"\n⚠️  No suitable packaging found for {weight_kg} kg")
        return

    # Step 2: Recommend services for e-commerce
    print(f"\n🛍️  E-commerce mode: {is_ecommerce}")

    recommended_codes = []
    if is_ecommerce:
        # Common e-commerce services
        ecommerce_services = [
            "INSURANCE",
            "TRYING_ON",
            "PART_DELIV",
            "SMS",
            "NOTIFY_ORDER_CREATED",
            "BAN_ATTACHMENT_INSPECTION"
        ]

        print("\n✓ Recommended services:")
        for code in ecommerce_services:
            service = get_service(code)
            if service:
                print(f"  • {service.name}")
                if service.auto_added:
                    print(f"    (added automatically)")
                else:
                    recommended_codes.append(code)

                if service.restrictions:
                    print(f"    ⚠️  {service.restrictions[:60]}...")

    # Step 3: Calculate delivery cost
    print("\n💰 Calculating delivery cost...")

    client = CdekClient(
        client_id=os.getenv("CDEK_CLIENT_ID"),
        client_secret=os.getenv("CDEK_CLIENT_SECRET"),
        test_mode=True
    )

    try:
        # Convert kg to grams for API
        weight_grams = int(weight_kg * 1000)

        # Parse box dimensions
        if box.dimensions:
            dims = [int(d) for d in box.dimensions.replace('x', ' ').replace('×', ' ').split()]
            length, width, height = dims[0], dims[1], dims[2]
        else:
            # Default dimensions
            length, width, height = 30, 20, 10

        # Calculate with recommended services
        services_to_add = [{"code": code} for code in recommended_codes[:2]]  # Add first 2

        result = await client.calculator.calculate_tariff(
            tariff_code=tariff_code,
            from_location=from_city_code,
            to_location=to_city_code,
            packages=[{
                "weight": weight_grams,
                "length": length,
                "width": width,
                "height": height
            }],
            services=services_to_add
        )

        print(f"\n✓ Calculation result:")
        print(f"  Total cost: {result.total_sum} {result.currency}")
        print(f"  Delivery cost: {result.delivery_sum} {result.currency}")
        print(f"  Delivery time: {result.period_min}-{result.period_max} days")

        if services_to_add:
            print(f"\n  Services included:")
            for svc in services_to_add:
                service = get_service(svc["code"])
                print(f"    • {service.name}")

        # Step 4: Show all available services
        print(f"\n📋 All available services for this delivery:")
        available = list_services(mode="warehouse-warehouse", max_weight=weight_kg)

        categories = {
            "Delivery": ["TAKE_SENDER", "DELIV_RECEIVER"],
            "Notifications": ["SMS", "NOTIFY_ORDER_CREATED", "NOTIFY_ORDER_DELIVERY"],
            "E-commerce": ["TRYING_ON", "PART_DELIV", "BAN_ATTACHMENT_INSPECTION"],
            "Special": ["GET_UP_FLOOR_BY_HAND", "GET_UP_FLOOR_BY_ELEVATOR", "ADULT_GOODS"]
        }

        for category, codes in categories.items():
            category_services = [s for s in available if s.code in codes]
            if category_services:
                print(f"\n  {category}:")
                for svc in category_services:
                    print(f"    • {svc.name} ({svc.code})")

        return {
            "box": box,
            "services": recommended_codes,
            "cost": result.total_sum,
            "currency": result.currency,
            "delivery_days": f"{result.period_min}-{result.period_max}"
        }

    except CdekError as e:
        print(f"\n❌ Error: {e.message}")
        if e.response_data:
            print(f"   Details: {e.response_data}")
        return None

    finally:
        await client.close()


async def main():
    """Run example scenarios."""

    # Scenario 1: Small e-commerce package
    print("\n" + "=" * 60)
    print("Scenario 1: Small e-commerce package (clothing)")
    print("=" * 60)
    await configure_delivery(
        weight_kg=1.5,
        from_city_code=270,  # Moscow
        to_city_code=44,     # Saint Petersburg
        is_ecommerce=True
    )

    # Scenario 2: Medium package
    print("\n\n" + "=" * 60)
    print("Scenario 2: Medium package (electronics)")
    print("=" * 60)
    await configure_delivery(
        weight_kg=4.5,
        from_city_code=270,  # Moscow
        to_city_code=44,     # Saint Petersburg
        is_ecommerce=True
    )

    # Scenario 3: Large package
    print("\n\n" + "=" * 60)
    print("Scenario 3: Large package (furniture)")
    print("=" * 60)
    await configure_delivery(
        weight_kg=15.0,
        from_city_code=270,  # Moscow
        to_city_code=44,     # Saint Petersburg
        is_ecommerce=False
    )


if __name__ == "__main__":
    asyncio.run(main())
