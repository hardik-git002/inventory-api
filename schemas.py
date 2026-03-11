from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Optional[str] = None
    is_available: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    category: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True