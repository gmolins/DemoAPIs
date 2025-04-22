from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Fake storage (importar desde item.py si es necesario)
fake_items_db = [
    {"id": 1, "name": "Item 1", "description": "Description for Item 1", "price": 100, "image": "/static/images/queso1.jpg"},
    {"id": 2, "name": "Item 2", "description": "Description for Item 2", "price": 200, "image": "/static/images/queso2.jpg"},
    {"id": 3, "name": "Item 3", "description": "Description for Item 3", "price": 300, "image": "/static/images/queso1.jpg"},
    {"id": 4, "name": "Item 4", "description": "Description for Item 4", "price": 400, "image": "/static/images/queso2.jpg"},
    {"id": 5, "name": "Item 5", "description": "Description for Item 5", "price": 500, "image": "https://www.escueladesarts.com/wp-content/uploads/tipos-y-variedades-de-quesos.jpg"}
]

@router.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("items.html", {"request": request, "items": fake_items_db})

@router.get("/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: int):
    item = next((item for item in fake_items_db if item["id"] == item_id), None)
    if not item:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})

@router.get("/fetch/{item_id}", response_class=HTMLResponse)
async def fetch_item_from_api(request: Request, item_id: int):
    """
    Este endpoint llama internamente al endpoint /api/items/{item_id} para obtener los datos del recurso.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/items/{item_id}")
            response.raise_for_status()  # Lanza una excepción si el código de estado no es 2xx
        item = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        raise HTTPException(status_code=e.response.status_code, detail="Error al obtener el recurso")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor interno")
    return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})

@router.get("/external/products", response_class=HTMLResponse)
async def fetch_products_from_fakestore(request: Request):
    """
    Este endpoint llama a la API de fakestoreapi para obtener los productos y renderiza una vista con ellos.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://fakestoreapi.com/products")
            response.raise_for_status()  # Lanza una excepción si el código de estado no es 2xx
        products = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error al obtener los productos")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error de conexión con la API externa")
    return templates.TemplateResponse("products.html", {"request": request, "products": products})