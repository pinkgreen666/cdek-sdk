"""Order type model for reference data."""

from pydantic import BaseModel


class OrderType(BaseModel):
    """CDEK order type information."""

    id: int
    name: str
