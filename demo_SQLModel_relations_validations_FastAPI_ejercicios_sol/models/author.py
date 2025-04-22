from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import EmailStr
from datetime import datetime, timezone

class AuthorBase(SQLModel):
    name: str = Field(index=True)  # Ensure name is indexed for faster lookups
    email: EmailStr = Field(index=True, unique=True)  # Use EmailStr for email validation

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="author")  # type: ignore
    is_deleted: bool = Field(default=False)  # Field to mark soft deletion
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Automatically set creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Automatically update timestamp

class AuthorCreate(AuthorBase):
    pass  # Excluir el campo id para la creación de un nuevo autor
