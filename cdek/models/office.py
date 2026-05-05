from pydantic import BaseModel, Field


class Phone(BaseModel):
    number: str = Field(description="Номер телефона")


class WorkTime(BaseModel):
    day: int = Field(description="День недели (1-7)")
    time: str = Field(description="Время работы (например, '10:00/20:00')")


class Location(BaseModel):
    country_code: str = Field(description="Код страны")
    region_code: int | None = Field(None, description="Код региона")
    region: str | None = Field(None, description="Название региона")
    city_code: int | None = Field(None, description="Код города")
    city: str | None = Field(None, description="Название города")
    fias_guid: str | None = Field(None, description="ФИАС GUID")
    postal_code: str | None = Field(None, description="Почтовый индекс")
    longitude: float | None = Field(None, description="Долгота")
    latitude: float | None = Field(None, description="Широта")
    address: str | None = Field(None, description="Адрес")
    address_full: str | None = Field(None, description="Полный адрес")
    city_uuid: str | None = Field(None, description="UUID города")


class DeliveryPoint(BaseModel):
    code: str = Field(description="Код ПВЗ")
    name: str = Field(description="Название ПВЗ")
    uuid: str = Field(description="UUID ПВЗ")
    address_comment: str | None = Field(None, description="Комментарий к адресу")
    nearest_station: str | None = Field(None, description="Ближайшая станция")
    nearest_metro_station: str | None = Field(None, description="Ближайшая станция метро")
    work_time: str = Field(description="Режим работы")
    phones: list[Phone] = Field(default_factory=list, description="Телефоны")
    email: str | None = Field(None, description="Email")
    note: str | None = Field(None, description="Примечание")
    type: str = Field(description="Тип офиса (PVZ, POSTAMAT)")
    owner_code: str | None = Field(None, description="Код владельца")
    take_only: bool = Field(description="Только пункт выдачи")
    is_handout: bool = Field(description="Является пунктом выдачи")
    is_reception: bool = Field(description="Есть приём заказов")
    is_dressing_room: bool = Field(description="Наличие примерочной")
    is_ltl: bool = Field(description="Работает с LTL")
    have_cashless: bool = Field(description="Есть терминал оплаты")
    have_cash: bool = Field(description="Есть приём наличных")
    have_fast_payment_system: bool = Field(description="Есть система быстрых платежей")
    allowed_cod: bool = Field(description="Разрешен наложенный платеж")
    site: str | None = Field(None, description="Сайт")
    work_time_list: list[WorkTime] = Field(default_factory=list, description="Список времени работы")
    work_time_exception_list: list = Field(default_factory=list, description="Исключения в режиме работы")
    weight_min: float | None = Field(None, description="Минимальный вес")
    weight_max: float | None = Field(None, description="Максимальный вес")
    location: Location = Field(description="Локация")
    ltl_acceptance_partners: bool = Field(description="Принимает LTL от партнеров")
    ltl_issuance_partners: bool = Field(description="Выдает LTL от партнеров")
    fulfillment: bool = Field(description="Офис с зоной фулфилмента")


class DeliveryPointsResponse(BaseModel):
    __root__: list[DeliveryPoint]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __len__(self):
        return len(self.__root__)
