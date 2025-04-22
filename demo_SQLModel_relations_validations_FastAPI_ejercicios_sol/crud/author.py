from sqlmodel import Session, select, join
from models.author import Author
from datetime import datetime, timezone

def create_author(session: Session, author: Author):
    existing_author = session.exec(select(Author).where(Author.email == author.email)).first()
    if existing_author:
        raise ValueError(f"An author with email '{author.email}' already exists.")
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

def get_authors(session: Session, limit: int = 10, offset: int = 0):
    statement = select(Author).where(Author.is_deleted == False).limit(limit).offset(offset)
    return session.exec(statement).all()

def get_author_by_id(session: Session, author_id: int):
    author = session.get(Author, author_id)
    return author if author and not author.is_deleted else None

def get_author_by_name(session: Session, name: str):
    statement = select(Author).where(Author.name == name, Author.is_deleted == False)
    return session.exec(statement).first()

def update_author(session: Session, author_id: int, author_data: dict):
    author = session.get(Author, author_id)
    if not author:
        return None
    for key, value in author_data.items():
        setattr(author, key, value)
    author.updated_at = datetime.now(timezone.utc)  # Update the timestamp
    session.commit()
    session.refresh(author)
    return author

def update_author_by_name(session: Session, name: str, author_data: dict):
    statement = select(Author).where(Author.name == name)
    author = session.exec(statement).first()
    if not author:
        return None
    for key, value in author_data.items():
        setattr(author, key, value)
    session.commit()
    session.refresh(author)
    return author

def delete_author(session: Session, author_id: int):
    author = session.get(Author, author_id)
    if author and not author.is_deleted:
        author.is_deleted = True
        session.commit()
    return author

def delete_author_by_name(session: Session, name: str):
    statement = select(Author).where(Author.name == name)
    author = session.exec(statement).first()
    if author:
        session.delete(author)
        session.commit()
    return author