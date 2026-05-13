from .services import (
    LocationService,
    OfficeService,
    CalculatorService,
    InternationalService,
    OrderService,
    DeliveryService,
    IntakeService,
    PrealertService,
    PrintService,
    RegistryService,
    PassportService,
    CheckService,
    ReverseService,
    PhotoService,
    WebhooksService,
)
from .http.async_http import AsyncHTTPClient


class CdekClient:
    def __init__(self, client_id: str, client_secret: str, test_mode: bool = False):
        self._http = AsyncHTTPClient(client_id, client_secret, test_mode)

        self.location = LocationService(self._http)
        self.office = OfficeService(self._http)
        self.calculator = CalculatorService(self._http)
        self.international = InternationalService(self._http)
        self.order = OrderService(self._http)
        self.delivery = DeliveryService(self._http)
        self.intake = IntakeService(self._http)
        self.prealert = PrealertService(self._http)
        self.print = PrintService(self._http)
        self.registry = RegistryService(self._http)
        self.passport = PassportService(self._http)
        self.check = CheckService(self._http)
        self.reverse = ReverseService(self._http)
        self.photo = PhotoService(self._http)
        self.webhooks = WebhooksService(self._http)

    async def close(self):
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()
