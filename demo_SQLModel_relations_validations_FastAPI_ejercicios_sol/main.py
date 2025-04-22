import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from db.database import create_db_and_tables
from routes import author, entry, category
import uvicorn
from sqlalchemy.exc import IntegrityError

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Omitir logs de SQLAlchemy
#logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

# Middleware para registrar solicitudes y respuestas
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request: {request.method} {request.url} Body: {body.decode('utf-8') if body else 'No Body'}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Crea la base de datos y las tablas al iniciar la aplicación
@asynccontextmanager
async def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Definir las rutas de la API
app.include_router(author.router, prefix="/api/authors", tags=["Authors"])
app.include_router(entry.router, prefix="/api/entries", tags=["Entries"])
app.include_router(category.router, prefix="/api/categories", tags=["Categories"])

# Manejo de excepciones globales con logging
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"IntegrityError: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": "A database integrity error occurred. Please check your data.", "error": str(exc)},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please contact support.", "error": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
