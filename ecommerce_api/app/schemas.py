from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    price: float
    stock: int
    image: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    item_id: int
    quantity: int
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    class Config:
        orm_mode = True
