from typing import Literal
from pydantic import BaseModel, Field


class CalculatorLocationDto(BaseModel):
    """
    Населённый пункт для вычислений тарифа

    Attributes:
        code (int): Код населенного пункта СДЭК (метод 'Список населенных пунктов')
        postal_code (str): Почтовый индекс (строка, например "101000")
        country_code (str): Код страны в формате ISO_3166-1_alpha-2 (по умолчанию 'RU')
        city (str): Название населенного пункта
        address (str): Строка адреса
        contragent_type (str): Тип контрагента (LEGAL_ENTITY - юр. лицо, INDIVIDUAL - физ. лицо)
        longitude (str): Долгота (от -180 до 180)
        latitude: Широта (от -90 до 90)
    """

    code: int | None = Field(
        None,
        description="Код населенного пункта СДЭК (метод 'Список населенных пунктов')",
    )
    postal_code: str | None = Field(None, max_length=255, description="Почтовый индекс")
    country_code: str | None = Field(
        None,
        max_length=2,
        description="Код страны в формате ISO_3166-1_alpha-2 (по умолчанию 'RU')",
    )
    city: str | None = Field(
        None, max_length=255, description="Название населенного пункта"
    )
    address: str | None = Field(None, max_length=255, description="Строка адреса")
    contragent_type: Literal["LEGAL_ENTITY", "INDIVIDUAL"] | None = Field(
        None,
        description="Тип контрагента, разрешённые значения: LEGAL_ENTITY - юридическое лицо; INDIVIDUAL - физическое лицо.",
    )
    longitude: float | None = Field(None, description="Долгота")
    latitude: float | None = Field(None, description="Широта")


class CalcPackageRequestDto(BaseModel):
    weight: int = Field(description="Общий вес (в граммах)")
    length: int | None = Field(
        None, description="Габариты упаковки. Длина (в сантиметрах)"
    )
    width: int | None = Field(
        None, description="Габариты упаковки. Ширина (в сантиметрах)"
    )
    height: int | None = Field(
        None, description="Габариты упаковки. Высота (в сантиметрах)"
    )
