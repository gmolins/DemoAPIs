from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlmodel import Session, select
from typing import Optional

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

@router.post("/", response_model=EntryRead, description="Create a new entry linked to an author.")
def create(entry: EntryCreate, session: Session = Depends(get_session)):
    """
    Create a new entry.
    - **title**: The title of the entry.
    - **content**: The content of the entry.
    - **author_name**: The name of the author associated with the entry.
    """
    try:
        if not entry.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty.")
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

@router.get("/", response_model=list[EntryRead], description="Retrieve all entries with pagination.")
def read_all(
    limit: int = Query(10, ge=1, description="The maximum number of entries to return."),
    offset: int = Query(0, ge=0, description="The number of entries to skip before starting to return results."),
    order_by: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    Retrieve all entries with pagination.
    - **limit**: The maximum number of entries to return.
    - **offset**: The number of entries to skip before starting to return results.
    - **order_by**: Optional. The field to order the results by (e.g., `title`, `created_at`).
    """
    try:
        return get_entries(session, limit=limit, offset=offset, order_by=order_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/search", response_model=list[EntryRead], description="Search entries by multiple criteria.")
def search_entries(
    title: Optional[str] = None,
    content: Optional[str] = None,
    author_name: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    Search entries by multiple criteria.
    - **title**: Optional. Filter by entry title.
    - **content**: Optional. Filter by entry content.
    - **author_name**: Optional. Filter by author's name.
    """
    try:
        statement = select(Entry).where(Entry.is_deleted == False)

        if title:
            statement = statement.where(Entry.title.contains(title))
        if content:
            statement = statement.where(Entry.content.contains(content))
        if author_name:
            statement = statement.join(Author).where(Author.name.contains(author_name), Author.is_deleted == False)

        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="No entries found matching the criteria.")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{entry_id}", response_model=EntryRead, description="Retrieve an entry by its unique ID.")
def read(entry_id: int, session: Session = Depends(get_session)):
    """
    Retrieve an entry by ID.
    - **entry_id**: The unique identifier of the entry.
    """
    try:
        entry = get_entry_by_id(session, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/title/{title}", response_model=EntryRead, description="Retrieve an entry by its title.")
def read_by_title(title: str, session: Session = Depends(get_session)):
    """
    Retrieve an entry by title.
    - **title**: The title of the entry.
    """
    try:
        entry = get_entry_by_title(session, title)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/author/{author_name}", response_model=list[EntryRead], description="Retrieve all entries by a specific author.")
def read_by_author_name(author_name: str, order_by: str = None, session: Session = Depends(get_session)):
    """
    Retrieve all entries by a specific author.
    - **author_name**: The name of the author.
    - **order_by**: Optional. The field to order the results by (e.g., `title`, `created_at`).
    """
    try:
        entries = get_entries_by_author_name(session, author_name, order_by=order_by)
        if not entries:
            raise HTTPException(status_code=404, detail=f"No entries found for author '{author_name}'")
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{entry_id}", response_model=Entry, description="Update an entry's details by its ID.")
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
    """
    Update an entry's details.
    - **entry_id**: The unique identifier of the entry.
    - **title**: The updated title of the entry.
    - **content**: The updated content of the entry.
    """
    try:
        if "id" in entry_data:
            raise HTTPException(status_code=400, detail="Updating 'id' is not allowed.")
        if "title" in entry_data and not entry_data["title"].strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty.")
        updated_entry = update_entry(session, entry_id, entry_data)
        if not updated_entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/title/{title}", response_model=Entry, description="Update an entry's details by its title.")
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
    """
    Update an entry's details by title.
    - **title**: The title of the entry to update.
    - **entry_data**: The updated details of the entry.
    """
    try:
        updated_entry = update_entry_by_title(session, title, entry_data)
        if not updated_entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{entry_id}", response_model=Entry, description="Soft delete an entry by its ID.")
def delete(entry_id: int, session: Session = Depends(get_session)):
    """
    Soft delete an entry.
    - **entry_id**: The unique identifier of the entry.
    """
    try:
        deleted_entry = delete_entry(session, entry_id)
        if not deleted_entry:
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found")
        return deleted_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/title/{title}", response_model=Entry, description="Soft delete an entry by its title.")
def delete_by_title(title: str, session: Session = Depends(get_session)):
    """
    Soft delete an entry by title.
    - **title**: The title of the entry to delete.
    """
    try:
        deleted_entry = delete_entry_by_title(session, title)
        if not deleted_entry:
            raise HTTPException(status_code=404, detail=f"Entry with title '{title}' not found")
        return deleted_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")