# FastAPI CRUD Demo

Este proyecto es una demostración didáctica de cómo montar una API con FastAPI utilizando un almacenamiento fake basado en un array en memoria. Incluye un CRUD completo para la entidad `Item` y vistas HTML renderizadas con Jinja2.

## Requisitos

- Python 3.8 o superior
- `pip` para instalar dependencias

## Instalación

1. Clona este repositorio o copia los archivos en tu máquina local.
2. Navega al directorio del proyecto:
   ```bash
   cd c:\Users\xandr\Documents\curso_python_mercedes\demos_fastAPI\app_crud_templates_fastAPI
   ```
3. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el servidor FastAPI:
   ```bash
   python main.py
   ```
   Esto iniciará el servidor en `http://127.0.0.1:8000`.

2. Accede a la documentación interactiva de la API en:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
app_crud_templates_fastAPI/
├── main.py                     # Punto de entrada principal de la aplicación
├── routes/                     # Contiene los routers para las rutas de la API y vistas web
│   ├── item.py                 # Rutas para el CRUD de la API
│   ├── item_web.py             # Rutas para las vistas HTML
├── schemas/                    # Define los esquemas Pydantic para validación de datos
│   ├── item.py                 # Esquemas para la entidad `Item`
├── middlewares/                # Contiene middlewares personalizados
│   ├── logging.py              # Middleware para registrar logs de solicitudes
│   ├── custom_header.py        # Middleware para añadir encabezados personalizados
│   ├── api_key.py              # Middleware para validar API KEY
│   ├── not_found_handler.py    # Middleware para manejar errores 404 en rutas `/api`
├── templates/                  # Plantillas HTML renderizadas con Jinja2
│   ├── items.html              # Lista de `Item`
│   ├── item_detail.html        # Detalles de un `Item`
│   ├── products.html           # Lista de productos de FakeStoreAPI
│   ├── 404.html                # Página de error 404
├── static/                     # Archivos estáticos como CSS y JS
│   ├── styles.css              # Hoja de estilos CSS
│   ├── script.js               # Archivo JavaScript (si es necesario)
├── requirements.txt            # Lista de dependencias del proyecto
├── README.md                   # Documentación del proyecto
```

## Endpoints de la API

### Base URL: `/api/items`

- **POST `/api/items/`**  
  Crea un nuevo `Item`.  
  **Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "price": 0
  }
  ```
  **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 0
  }
  ```

- **GET `/api/items/{item_id}`**  
  Obtiene un `Item` por su ID.  
  **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 0
  }
  ```

- **PUT `/api/items/{item_id}`**  
  Actualiza un `Item` existente.  
  **Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "price": 0
  }
  ```
  **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 0
  }
  ```

- **DELETE `/api/items/{item_id}`**  
  Elimina un `Item` por su ID.  
  **Response**:
  ```json
  {
    "message": "Item deleted successfully"
  }
  ```

## Nuevas Vistas

Este proyecto incluye vistas HTML renderizadas con Jinja2. Las vistas disponibles son:

- **GET `/items/`**  
  Renderiza una lista de todos los `Item`.
- **GET `/items/{item_id}`**  
  Renderiza los detalles de un `Item` específico.
- **GET `/items/fetch/{item_id}`**  
  Llama internamente al endpoint `/api/items/{item_id}` para obtener los datos y renderiza los detalles del `Item`.
- **GET `/items/external/products`**  
  Llama a la API externa `https://fakestoreapi.com/products` para obtener productos y renderiza una lista de ellos.

Las plantillas HTML se encuentran en el directorio `templates`.

## Manejo de Errores 404

### Middleware `NotFoundHandlerMiddleware`

El middleware `NotFoundHandlerMiddleware` maneja errores 404 para las rutas que comienzan con `/api`. Cuando un recurso no se encuentra, devuelve un JSON con el siguiente formato:

```json
{
  "error": "Not Found",
  "message": "The requested resource was not found.",
  "hint": "Check the URL or contact support if the issue persists."
}
```

### Renderización de `404.html`

Para las rutas que no comienzan con `/api`, como las vistas HTML, los errores 404 renderizan la plantilla `404.html`. Esto asegura que los usuarios vean una página amigable cuando intentan acceder a un recurso inexistente.

## Explicación del Código

### `main.py`

Este archivo inicializa la aplicación FastAPI, registra los routers y configura middlewares. También incluye la directiva `if __name__ == "__main__":` para ejecutar el servidor directamente desde el archivo.

### `schemas/item.py`

Define los esquemas Pydantic para la validación de datos. Incluye:
- `ItemBase`: Esquema base con los campos `name`, `description` y `price`.
- `ItemCreate`: Hereda de `ItemBase` y se usa para crear nuevos `Item`.
- `ItemResponse`: Hereda de `ItemBase` y añade el campo `id` para las respuestas.

### `routes/item.py`

Contiene las rutas para el CRUD de `Item`. Utiliza un array en memoria (`fake_items_db`) para almacenar los datos. Las operaciones incluyen:
- Crear un nuevo `Item` (`POST`).
- Leer un `Item` por ID (`GET`).
- Actualizar un `Item` por ID (`PUT`).
- Eliminar un `Item` por ID (`DELETE`).

### `routes/item_web.py`

Contiene las rutas para las vistas HTML. Incluye:
- Renderización de la lista de `Item`.
- Renderización de los detalles de un `Item`.
- Llamadas internas a la API para obtener datos de `Item`.
- Llamadas a la API externa `FakeStoreAPI` para obtener productos.

### `middlewares/not_found_handler.py`

Middleware que maneja errores 404 para rutas que comienzan con `/api`. Devuelve un JSON con un mensaje de error personalizado.

### `requirements.txt`

Lista las dependencias necesarias para ejecutar el proyecto:
- `fastapi`: Framework para construir la API.
- `uvicorn`: Servidor ASGI para ejecutar la aplicación.
- `pydantic`: Para la validación de datos.
- `jinja2`: Para renderizar plantillas HTML.

## Notas

- Este proyecto utiliza un almacenamiento fake en memoria, por lo que los datos no se persisten entre ejecuciones.
- En un entorno real, se recomienda usar una base de datos como SQLite, PostgreSQL o MySQL.

## Próximos Pasos

- Implementar una base de datos real.
- Añadir autenticación y autorización.
- Crear tests automatizados para la API.