from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from typing import List
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# In-memory books storage
books = [
    {"title": "1984", "author": "George Orwell"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
]

# In-memory users storage
users = [
    {"username": "user0", "email": "user0@example.com", "password": "pass123"},
    {"username": "user1", "email": "user1@example.com", "password": "pass123"},
    {"username": "user2", "email": "user2@example.com", "password": "pass123"}
]

# Pydantic models
class Book(BaseModel):
    title: str
    author: str

class LoginData(BaseModel):
    username: str
    password: str

# Helper function to decode JWT
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency to verify JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    return decode_jwt(token)

# Endpoints
@app.post("/login")
def login(data: LoginData):
    user = next((u for u in users if u["username"] == data.username and u["password"] == data.password), None)
    if user:
        expiration = datetime.now() + timedelta(minutes=5) # Token valid for 5 minutes
        token = jwt.encode({"username": user["username"], "exp": expiration}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/books", response_model=List[Book])
def get_books(token: dict = Depends(verify_token)):
    return books

@app.post("/books")
def add_book(book: Book, token: dict = Depends(verify_token)):
    books.append(book)
    return {"message": "Book added successfully"}

@app.put("/books")
def update_book(index: int, book: Book, token: dict = Depends(verify_token)):
    if 0 <= index < len(books):
        books[index] = book
        return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books")
def delete_book(index: int, token: dict = Depends(verify_token)):
    if 0 <= index < len(books):
        books.pop(index)
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
