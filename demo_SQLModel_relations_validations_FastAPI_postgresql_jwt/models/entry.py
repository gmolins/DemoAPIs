from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.author import Author

class EntryBase(SQLModel):
    title: str = Field(index=True, unique=True)  # Make title unique and indexed
    content: str

class Entry(EntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="author.id")
    author: Optional["Author"] = Relationship(back_populates="entries") 

class EntryCreate(EntryBase):
    author_name: str 

class EntryRead(EntryBase):
    id: int
    author: Author
