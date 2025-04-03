from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List
import uvicorn

app = FastAPI()

# Modelo de datos para un usuario
class User(BaseModel):
     #id: int
     name: str = Field(..., min_length=3, max_length=50, description="El nombre debe tener entre 3 y 50 caracteres")
     email: EmailStr
     age: int = Field(..., gt=0, description="La edad debe ser mayor a 0")

fake_db: List[User] = [
     User(id=1, name="Alice Smith", email="alice.smith@example.com", age=30),
     User(id=2, name="Bob Johnson", email="bob.johnson@example.com", age=25),
     User(id=3, name="Charlie Brown", email="charlie.brown@example.com", age=35),
     User(id=4, name="Diana Prince", email="diana.prince@example.com", age=28),
     User(id=5, name="Ethan Hunt", email="ethan.hunt@example.com", age=40),
]

# Variable global para el último ID usado
last_id = max(user["id"] for user in fake_db)

# Crear un usuario
@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: User):
     global last_id
     for existing_user in fake_db:
          if existing_user.email == user.email:
                raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
     last_id += 1
     user["id"] = last_id
     fake_db.append(user)
     return user

# Leer todos los usuarios
@app.get("/users/", response_model=List[User])
async def read_users():
     return fake_db

# Leer un usuario por ID
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
     for user in fake_db:
          if user["id"] == user_id:
                return user
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Actualizar un usuario
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
     for index, user in enumerate(fake_db):
          if user["id"] == user_id:
                fake_db[index] = updated_user
                return updated_user
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Eliminar un usuario
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
     for index, user in enumerate(fake_db):
          if user["id"] == user_id:
                del fake_db[index]
                return
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

if __name__ == "__main__":
     uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)