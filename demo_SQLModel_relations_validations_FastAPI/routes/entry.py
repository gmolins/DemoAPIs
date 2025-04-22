from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from db.database import get_session
from models.entry import Entry, EntryCreate, EntryRead
from models.author import Author
from crud.author import get_author_by_name
from crud.entry import (
    create_entry,
    get_entries,
    get_entry_by_id,
    update_entry,
    delete_entry,
    get_entry_by_title,
    update_entry_by_title,
    delete_entry_by_title,
    get_entries_by_author_name,
)

router = APIRouter()

@router.post("/", response_model=EntryRead)
def create(entry: EntryCreate, session: Session = Depends(get_session)):
    try:
        # Use the function from CRUD to get the author by name
        author = get_author_by_name(session, entry.author_name)
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with name '{entry.author_name}' not found")
        
        # Create the entry with the author's ID
        entry_data = Entry(**entry.model_dump(exclude={"author_name"}), author_id=author.id)
        created_entry = create_entry(session, entry_data)
        session.refresh(created_entry)  # Refresh to load relationships
        return created_entry
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[EntryRead])
def read_all(session: Session = Depends(get_session)):
    try:
        return get_entries(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{entry_id}", response_model=EntryRead)
def read(entry_id: int, session: Session = Depends(get_session)):
    try:
        entry = get_entry_by_id(session, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/title/{title}", response_model=EntryRead)
def read_by_title(title: str, session: Session = Depends(get_session)):
    try:
        entry = get_entry_by_title(session, title)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/author/{author_name}", response_model=list[EntryRead])
def read_by_author_name(author_name: str, session: Session = Depends(get_session)):
    try:
        entries = get_entries_by_author_name(session, author_name)
        if not entries:
            raise HTTPException(status_code=404, detail=f"No entries found for author '{author_name}'")
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{entry_id}", response_model=Entry)
def update(
    entry_id: int,
    entry_data: dict = Body(
        ...,
        example={
            "title": "Updated Entry Title",
            "content": "Updated content for the entry"
        }
    ),
    session: Session = Depends(get_session),
):
    try:
        updated_entry = update_entry(session, entry_id, entry_data)
        if not updated_entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/title/{title}", response_model=Entry)
def update_by_title(
    title: str,
    entry_data: dict = Body(
        ...,
        example={
            "title": "Updated Entry Title",
            "content": "Updated content for the entry"
        }
    ),
    session: Session = Depends(get_session),
):
    try:
        updated_entry = update_entry_by_title(session, title, entry_data)
        if not updated_entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{entry_id}", response_model=Entry)
def delete(entry_id: int, session: Session = Depends(get_session)):
    try:
        deleted_entry = delete_entry(session, entry_id)
        if not deleted_entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return deleted_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/title/{title}", response_model=Entry)
def delete_by_title(title: str, session: Session = Depends(get_session)):
    try:
        deleted_entry = delete_entry_by_title(session, title)
        if not deleted_entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return deleted_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")