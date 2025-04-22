from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.author import Author
from models.entry import Entry
from models.user import User
from auth.hashing import hash_password  # Importamos la función para hashear contraseñas

def seed_data():
    # Borrar la base de datos y las tablas existentes
    drop_db_and_tables() 
    # Crear la base de datos y las tablas
    create_db_and_tables()

    with Session(engine) as session:
        # Crear autores
        try:
            author1 = Author(name="Author One", email="author1@example.com")
            author2 = Author(name="Author Two", email="author2@example.com")
            session.add_all([author1, author2])
            session.commit()
        except Exception as e:
            print(f"Error creating authors: {e}")

        # Crear entradas linkadas a autores
        try:
            entry1 = Entry(title="Entry One", content="Content for entry one", author_id=author1.id)
            entry2 = Entry(title="Entry Two", content="Content for entry two", author_id=author2.id)
            entry3 = Entry(title="Entry Three", content="Content for entry three", author_id=author1.id)
            session.add_all([entry1, entry2, entry3])
            session.commit()
        except Exception as e:
            print(f"Error creating entries: {e}")

        # Crear usuarios
        try:
            user1 = User(username="user1", email="user1@example.com", hashed_password=hash_password("password1"))
            user2 = User(username="user2", email="user2@example.com", hashed_password=hash_password("password2"))
            session.add_all([user1, user2])
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}")

if __name__ == "__main__":
    seed_data()
