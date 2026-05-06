"""Service model for reference data."""

from pydantic import BaseModel
from typing import Optional, List


class Service(BaseModel):
    """CDEK additional service information."""

    code: str
    name: str
    description: str
    modes: Optional[List[str]] = None
    weight_limit: Optional[float] = None
    max_weight: Optional[float] = None
    dimensions: Optional[str] = None
    requires_parameter: bool = False
    auto_added: bool = False
    restrictions: Optional[str] = None
