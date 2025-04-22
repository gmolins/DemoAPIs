from fastapi import APIRouter, HTTPException, Depends, status, Query
from schemas.item import ItemCreate, ItemResponse
from middlewares.api_key import api_key_dependency
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Fake storage
fake_items_db = [
    {"id": 1, "name": "Item 1", "description": "Description for Item 1", "price": 100},
    {"id": 2, "name": "Item 2", "description": "Description for Item 2", "price": 200},
    {"id": 3, "name": "Item 3", "description": "Description for Item 3", "price": 300},
    {"id": 4, "name": "Item 4", "description": "Description for Item 4", "price": 400},
    {"id": 5, "name": "Item 5", "description": "Description for Item 5", "price": 500},
]
item_id_counter = 6  # Start counter after the last ID

@router.get("/", response_model=list[ItemResponse])
def read_items():
    return fake_items_db

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    for item in fake_items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(api_key_dependency)])
def create_item(item: ItemCreate):
    """
    Este endpoint está protegido con la API KEY.
    Solo se puede acceder si se proporciona una API KEY válida como parámetro de consulta.
    """
    global item_id_counter
    new_item = {"id": item_id_counter, **item.dict()}
    fake_items_db.append(new_item)
    item_id_counter += 1
    return new_item

@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(api_key_dependency)])
def update_item(item_id: int, item: ItemCreate):
    """
    Este endpoint está protegido con la API KEY.
    Solo se puede acceder si se proporciona una API KEY válida como parámetro de consulta.
    """
    for stored_item in fake_items_db:
        if stored_item["id"] == item_id:
            stored_item.update(item.dict())
            return stored_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(api_key_dependency)])
def delete_item(item_id: int):
    """
    Este endpoint está protegido con la API KEY.
    Solo se puede acceder si se proporciona una API KEY válida como parámetro de consulta.
    DELETE /items/{item_id}
    """
    for index, stored_item in enumerate(fake_items_db):
        if stored_item["id"] == item_id:
            del fake_items_db[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/{item_id}/filter", response_model=list[ItemResponse])
def filter_items(
    item_id: int,
    min_price: int = Query(0, description="Minimum price to filter items"),
    max_price: int = Query(1000, description="Maximum price to filter items"),
):
    """
    Endpoint que utiliza parámetros de ruta y parámetros de consulta.
    Filtra los items por rango de precio.
    GET /items/{item_id}/filter?min_price=0&max_price=1000
    """
    filtered_items = [
        item for item in fake_items_db
        if item["id"] == item_id and min_price <= item["price"] <= max_price
    ]
    if not filtered_items:
        raise HTTPException(status_code=404, detail="No items found matching the criteria")
    return filtered_items
