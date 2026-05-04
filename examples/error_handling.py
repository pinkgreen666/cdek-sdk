"""Example usage of CDEK SDK error handling."""

import asyncio
from cdek import CdekClient
from cdek.exceptions import (
    CdekError,
    CdekAuthError,
    CdekValidationError,
    CdekNotFoundError,
    CdekServerError,
    CdekTimeoutError,
    CdekNetworkError,
)


async def example_basic_error_handling():
    """Basic error handling - catch all CDEK errors."""
    client = CdekClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        test_mode=True
    )

    try:
        result = await client.calculator.calculate_tariff(
            tariff_code=1,
            from_location={"code": 44},
            to_location={"code": 270},
            packages=[{"weight": 1000, "length": 10, "width": 10, "height": 10}]
        )
        print(f"Delivery cost: {result}")
    except CdekError as e:
        print(f"CDEK API error: {e.message}")
        print(f"Status code: {e.status_code}")
        print(f"Response data: {e.response_data}")
    finally:
        await client.close()


async def example_specific_error_handling():
    """Handle specific error types differently."""
    client = CdekClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        test_mode=True
    )

    try:
        result = await client.order.create_order({
            "type": 1,
            "number": "TEST-ORDER-001",
            "tariff_code": 1,
            "sender": {"name": "Test Sender"},
            "recipient": {"name": "Test Recipient"},
            "from_location": {"code": 44},
            "to_location": {"code": 270},
            "packages": [{"number": "1", "weight": 1000}]
        })
        print(f"Order created: {result}")

    except CdekAuthError as e:
        print(f"Authentication failed: {e.message}")
        print("Check your credentials")

    except CdekValidationError as e:
        print(f"Invalid request data: {e.message}")
        print(f"Details: {e.response_data}")

    except CdekServerError as e:
        print(f"CDEK server error: {e.message}")
        print(f"Status: {e.status_code}")
        print("Try again later or contact support")

    except CdekTimeoutError as e:
        print(f"Request timed out: {e.message}")
        print("Check your network connection")

    except CdekNetworkError as e:
        print(f"Network error: {e.message}")
        print("Check your internet connection")

    except CdekError as e:
        print(f"Unexpected CDEK error: {e.message}")

    finally:
        await client.close()


async def example_retry_on_server_error():
    """Retry logic for server errors."""
    client = CdekClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        test_mode=True
    )

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            result = await client.location.get_location_suggest_cities("Moscow", "RU")
            print(f"Success: {result}")
            break

        except CdekServerError as e:
            if attempt < max_retries - 1:
                print(f"Server error (attempt {attempt + 1}/{max_retries}): {e.message}")
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Failed after {max_retries} attempts: {e.message}")
                raise

        except CdekError as e:
            print(f"Non-retryable error: {e.message}")
            raise

    await client.close()


async def example_graceful_degradation():
    """Gracefully handle errors without crashing the application."""
    client = CdekClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        test_mode=True
    )

    cities = ["Moscow", "Saint Petersburg", "Novosibirsk"]
    results = []

    for city in cities:
        try:
            result = await client.location.get_location_suggest_cities(city, "RU")
            results.append({"city": city, "data": result, "error": None})
        except CdekError as e:
            print(f"Failed to fetch {city}: {e.message}")
            results.append({"city": city, "data": None, "error": str(e)})

    await client.close()

    print(f"Successfully fetched {sum(1 for r in results if r['data'])} out of {len(cities)} cities")
    return results


if __name__ == "__main__":
    print("Example 1: Basic error handling")
    asyncio.run(example_basic_error_handling())

    print("\nExample 2: Specific error handling")
    asyncio.run(example_specific_error_handling())

    print("\nExample 3: Retry on server error")
    asyncio.run(example_retry_on_server_error())

    print("\nExample 4: Graceful degradation")
    asyncio.run(example_graceful_degradation())
