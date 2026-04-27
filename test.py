import asyncio
from sdk.client import CdekClient

client = CdekClient(
    "REMOVED", "REMOVED", True
)


async def test():
    await client.location.get_location_suggest_cities("Москва", None)


if __name__ == "__main__":
    asyncio.run(test())
