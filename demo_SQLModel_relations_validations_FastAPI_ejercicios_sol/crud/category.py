from sqlmodel import Session, select
from models.category import Category

def create_category(session: Session, category: Category):
    existing_category = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing_category:
        raise ValueError(f"A category with name '{category.name}' already exists.")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

def get_categories(session: Session):
    return session.exec(select(Category)).all()

def get_category_by_id(session: Session, category_id: int):
    return session.get(Category, category_id)

def delete_category(session: Session, category_id: int):
    category = session.get(Category, category_id)
    if category:
        session.delete(category)
        session.commit()
    return category
