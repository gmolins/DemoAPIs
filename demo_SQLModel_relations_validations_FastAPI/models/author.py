from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import EmailStr

class AuthorBase(SQLModel):
    name: str = Field(..., min_length=3, max_length=100, description="Author name cant be empty")
    email: EmailStr = Field(index=True, unique=True)  # Use EmailStr for email validation

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="author")  # type: ignore

class AuthorCreate(AuthorBase):
    pass  # Excluir el campo id para la creación de un nuevo autor
