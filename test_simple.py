from cdek.client import CdekClient
import asyncio


async def main():
    client = CdekClient(
        "REMOVED", "REMOVED", True
    )
    await client._http._auth()
    print(client._http._access_token)
    await client.location.get_location_suggest_cities("Москва", None)


if __name__ == "__main__":
    asyncio.run(main())
