from sqlmodel import Session, select
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

def get_entries(session: Session):
    return session.exec(select(Entry)).all()

def get_entry_by_id(session: Session, entry_id: int):
    return session.get(Entry, entry_id)

def get_entry_by_title(session: Session, title: str):
    statement = select(Entry).where(Entry.title == title)
    return session.exec(statement).first()

def update_entry(session: Session, entry_id: int, entry_data: dict):
    entry = session.get(Entry, entry_id)
    if not entry:
        return None
    for key, value in entry_data.items():
        setattr(entry, key, value)
    session.commit()
    session.refresh(entry)
    return entry

def update_entry_by_title(session: Session, title: str, entry_data: dict):
    statement = select(Entry).where(Entry.title == title)
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
    if entry:
        session.delete(entry)
        session.commit()
    return entry

def delete_entry_by_title(session: Session, title: str):
    statement = select(Entry).where(Entry.title == title)
    entry = session.exec(statement).first()
    if entry:
        session.delete(entry)
        session.commit()
    return entry

def get_entries_by_author_name(session: Session, author_name: str):
    author = get_author_by_name(session, author_name)
    if not author:
        return []
    statement = select(Entry).where(Entry.author_id == author.id)
    return session.exec(statement).all()