from sqlmodel import Session, select, join
from datetime import datetime
from models.entry import Entry
from models.author import Author
from crud.author import get_author_by_name

def create_entry(session: Session, entry: Entry):
    existing_entry = session.exec(select(Entry).where(Entry.title == entry.title)).first()
    if existing_entry:
        raise ValueError(f"An entry with title '{entry.title}' already exists.")
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

def get_entries(session: Session, limit: int = 10, offset: int = 0, order_by: str = None):
    statement = select(Entry).where(Entry.is_deleted == False).limit(limit).offset(offset)
    if order_by:
        statement = statement.order_by(getattr(Entry, order_by))
    return session.exec(statement).all()

def get_entry_by_id(session: Session, entry_id: int):
    entry = session.get(Entry, entry_id)
    return entry if entry and not entry.is_deleted else None

def get_entry_by_title(session: Session, title: str):
    statement = select(Entry).where(Entry.title == title, Entry.is_deleted == False)
    return session.exec(statement).first()

def update_entry(session: Session, entry_id: int, entry_data: dict):
    entry = session.get(Entry, entry_id)
    if not entry or entry.is_deleted:
        return None
    for key, value in entry_data.items():
        setattr(entry, key, value)
    entry.updated_at = datetime.utcnow()  # Manually update the timestamp
    session.commit()
    session.refresh(entry)
    return entry

def update_entry_by_title(session: Session, title: str, entry_data: dict):
    statement = select(Entry).where(Entry.title == title, Entry.is_deleted == False)
    entry = session.exec(statement).first()
    if not entry:
        return None
    for key, value in entry_data.items():
        setattr(entry, key, value)
    session.commit()
    session.refresh(entry)
    return entry

def delete_entry(session: Session, entry_id: int):
    entry = session.get(Entry, entry_id)
    if entry and not entry.is_deleted:
        entry.is_deleted = True
        session.commit()
    return entry

def delete_entry_by_title(session: Session, title: str):
    statement = select(Entry).where(Entry.title == title, Entry.is_deleted == False)
    entry = session.exec(statement).first()
    if entry:
        entry.is_deleted = True
        session.commit()
    return entry

def get_entries_by_author_name(session: Session, author_name: str, order_by: str = None):
    statement = (
        select(Entry)
        .join(Author, Entry.author_id == Author.id)
        .where(Author.name == author_name, Entry.is_deleted == False, Author.is_deleted == False)
    )
    if order_by:
        statement = statement.order_by(getattr(Entry, order_by))
    return session.exec(statement).all()