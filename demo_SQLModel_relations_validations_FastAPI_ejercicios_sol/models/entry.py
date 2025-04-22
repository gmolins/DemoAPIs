from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.author import Author
from models.category import Category
from datetime import datetime, timezone

class EntryBase(SQLModel):
    title: str = Field(index=True, unique=True)  # Ensure title is indexed for faster lookups
    content: str

class Entry(EntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="author.id")
    author: Optional["Author"] = Relationship(back_populates="entries") 
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="entries")
    is_deleted: bool = Field(default=False)  # Field to mark soft deletion
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Automatically set creation timestamp
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Automatically update timestamp

class EntryCreate(EntryBase):
    author_name: str 

class EntryRead(EntryBase):
    id: int
    author: Author
