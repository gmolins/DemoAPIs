from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlmodel import Session
from db.database import get_session
from models.author import Author, AuthorCreate
from crud.author import (
    create_author,
    get_authors,
    get_author_by_id,
    get_author_by_name,
    update_author,
    delete_author,
    update_author_by_name,
    delete_author_by_name,
)

router = APIRouter()

@router.post("/", response_model=Author, description="Create a new author with a unique email.")
def create(author: AuthorCreate, session: Session = Depends(get_session)):
    """
    Create a new author.
    - **name**: The name of the author.
    - **email**: A unique email address for the author.
    """
    try:
        if not author.email.strip():
            raise HTTPException(status_code=400, detail="Email cannot be empty.")
        author_data = Author(**author.model_dump())
        return create_author(session, author_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[Author], description="Retrieve all authors with pagination.")
def read_all(
    limit: int = Query(10, ge=1, description="The maximum number of authors to return."),
    offset: int = Query(0, ge=0, description="The number of authors to skip before starting to return results."),
    session: Session = Depends(get_session)
):
    """
    Retrieve all authors with pagination.
    - **limit**: The maximum number of authors to return.
    - **offset**: The number of authors to skip before starting to return results.
    """
    try:
        return get_authors(session, limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{author_id}", response_model=Author, description="Retrieve an author by their unique ID.")
def read(author_id: int, session: Session = Depends(get_session)):
    """
    Retrieve an author by ID.
    - **author_id**: The unique identifier of the author.
    """
    try:
        author = get_author_by_id(session, author_id)
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/name/{name}", response_model=Author, description="Retrieve an author by their name.")
def read_by_name(name: str, session: Session = Depends(get_session)):
    """
    Retrieve an author by name.
    - **name**: The name of the author.
    """
    try:
        author = get_author_by_name(session, name)
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{author_id}", response_model=Author, description="Update an author's details by their ID.")
def update(
    author_id: int,
    author_data: dict = Body(
        ...,
        example={
            "name": "Updated Author Name",
            "email": "updated_email@example.com"
        }
    ),
    session: Session = Depends(get_session),
):
    """
    Update an author's details.
    - **author_id**: The unique identifier of the author.
    - **name**: The updated name of the author.
    - **email**: The updated email address of the author.
    """
    try:
        if "id" in author_data:
            raise HTTPException(status_code=400, detail="Updating 'id' is not allowed.")
        if "email" in author_data and not author_data["email"].strip():
            raise HTTPException(status_code=400, detail="Email cannot be empty.")
        updated_author = update_author(session, author_id, author_data)
        if not updated_author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/name/{name}", response_model=Author, description="Update an author's details by their name.")
def update_by_name(
    name: str,
    author_data: dict = Body(
        ...,
        example={
            "name": "Updated Author Name",
            "email": "updated_email@example.com"
        }
    ),
    session: Session = Depends(get_session),
):
    """
    Update an author's details by name.
    - **name**: The name of the author to update.
    - **author_data**: The updated details of the author.
    """
    try:
        if "id" in author_data:
            raise HTTPException(status_code=400, detail="Updating 'id' is not allowed.")
        if "email" in author_data and not author_data["email"].strip():
            raise HTTPException(status_code=400, detail="Email cannot be empty.")
        updated_author = update_author_by_name(session, name, author_data)
        if not updated_author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return updated_author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{author_id}", response_model=Author, description="Soft delete an author by their ID.")
def delete(author_id: int, session: Session = Depends(get_session)):
    """
    Soft delete an author.
    - **author_id**: The unique identifier of the author.
    """
    try:
        deleted_author = delete_author(session, author_id)
        if not deleted_author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return deleted_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/name/{name}", response_model=Author, description="Soft delete an author by their name.")
def delete_by_name(name: str, session: Session = Depends(get_session)):
    """
    Soft delete an author by name.
    - **name**: The name of the author to delete.
    """
    try:
        deleted_author = delete_author_by_name(session, name)
        if not deleted_author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return deleted_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")