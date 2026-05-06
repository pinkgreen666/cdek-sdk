"""Delivery mode model."""

from pydantic import BaseModel


class DeliveryMode(BaseModel):
    """Delivery mode model.

    Attributes:
        code: Delivery mode code
        name: Delivery mode name (Russian)
    """

    code: int
    name: str
