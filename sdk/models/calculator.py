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


class CalcAdditionalServiceDto(BaseModel):
    code: str | None = Field(
        None, max_length=255, description="Тип дополнительной услуги"
    )
    parameter: str | None = Field(
        None,
        max_length=255,
        description="Параметр дополнительной услуги \
        1. Количество для услуг PACKAGE_1, PACKAGE_A_2_LIGHT_EXPRESS, PACKAGE_A_3_LIGHT_EXPRESS, \
        PACKAGE_A_4_LIGHT_EXPRESS, PACKAGE_A_5_LIGHT_EXPRESS, CARTON_BOX_XS, CARTON_BOX_S, CARTON_BOX_M, \
        CARTON_BOX_2KG, CARTON_BOX_3KG, CARTON_BOX_5KG, CARTON_BOX_10KG, CARTON_BOX_XL_18_KILOS, \
        CARTON_BOX_20KG, CARTON_BOX_30KG, CARTON_FILLER, XL_BOX_INNER_CRATE, 20_KG_BOX_INNER_CRATE, \
        30_KG_BOX_INNER_CRATE (для всех типов заказа) \
        2. Объявленная стоимость заказа для услуги INSURANCE (для всех типов заказа) \
        3. Длина для услуг BUBBLE_WRAP, WASTE_PAPER (для всех типов заказа) \
        4. Номер телефона для услуги SMS",
    )
