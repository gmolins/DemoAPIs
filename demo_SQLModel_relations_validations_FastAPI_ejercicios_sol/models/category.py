from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="category")  # type: ignore

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
