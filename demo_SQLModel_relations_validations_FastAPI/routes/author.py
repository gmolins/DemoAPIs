from fastapi import APIRouter, Depends, HTTPException, Body
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

@router.post("/", response_model=Author)
def create(author: AuthorCreate, session: Session = Depends(get_session)):
    try:
        author_data = Author(**author.model_dump())
        return create_author(session, author_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[Author])
def read_all(session: Session = Depends(get_session)):
    try:
        return get_authors(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{author_id}", response_model=Author)
def read(author_id: int, session: Session = Depends(get_session)):
    try:
        author = get_author_by_id(session, author_id)
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/name/{name}", response_model=Author)
def read_by_name(name: str, session: Session = Depends(get_session)):
    try:
        author = get_author_by_name(session, name)
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{author_id}", response_model=Author)
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
    try:
        updated_author = update_author(session, author_id, author_data)
        if not updated_author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/name/{name}", response_model=Author)
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
    try:
        updated_author = update_author_by_name(session, name, author_data)
        if not updated_author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{author_id}", response_model=Author)
def delete(author_id: int, session: Session = Depends(get_session)):
    try:
        deleted_author = delete_author(session, author_id)
        if not deleted_author:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        return deleted_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/name/{name}", response_model=Author)
def delete_by_name(name: str, session: Session = Depends(get_session)):
    try:
        deleted_author = delete_author_by_name(session, name)
        if not deleted_author:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
        return deleted_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")