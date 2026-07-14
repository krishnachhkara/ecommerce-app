from pydantic import BaseModel,Field,ConfigDict
from decimal import Decimal

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id:int
    product_id: int
    name: str
    price: Decimal
    quantity: int
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: Decimal
    # Optional but recommended for consistency ->
    model_config = ConfigDict(from_attributes=True)  
