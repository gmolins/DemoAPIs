from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True  # Reemplaza orm_mode en Pydantic v2

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
