from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes.item import router as item_router
from routes.item_web import router as item_web_router
from middlewares.logging import log_requests
from middlewares.custom_header import add_custom_header
from middlewares.api_key import api_key_dependency
from middlewares.not_found_handler import NotFoundHandlerMiddleware

app = FastAPI()
# app = FastAPI(redirect_slashes=False)  # Deshabilitar redirecciones automáticas. Evita el 307 temporary redirect

# Configuración de Jinja2
templates = Jinja2Templates(directory="templates")
# Configuración de archivos estáticos con el prefijo "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar middlewares
app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)
app.add_middleware(NotFoundHandlerMiddleware)
#Aplica de manera global el middleware de la API KEY a todos los endpoints
# app.add_middleware(api_key_dependency)
#app.router.dependencies.append(Depends(api_key_dependency))

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI CRUD demo!"}

# Proteger un endpoint específico con la API KEY
@app.get("/protected", dependencies=[Depends(api_key_dependency)])
def protected_endpoint():
    """
    Este endpoint está protegido con la API KEY.
    Solo se puede acceder si se proporciona una API KEY válida como parámetro de consulta.
    """
    return {"message": "You have access to the protected endpoint!"}

# Registrar routers
app.include_router(item_router, prefix="/api/items", tags=["API Items"])
app.include_router(item_web_router, prefix="/items", tags=["Web Items"])

# Proteger todos los endpoints del router con la API KEY
# app.include_router(item_router, prefix="/items", tags=["Items"], dependencies=[Depends(api_key_dependency)])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
