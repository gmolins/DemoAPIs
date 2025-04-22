# Demo de Autenticación con JWT usando FastAPI

Este proyecto es una demostración de cómo implementar autenticación con JWT en una API creada con FastAPI. La API incluye endpoints protegidos que requieren un token JWT para acceder.

## Requisitos

- Python 3.8 o superior
- `pip` para instalar dependencias

## Instalación

1. Crea un entorno virtual (opcional pero recomendado).
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias necesarias.
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. Inicia el servidor FastAPI.
   ```bash
   uvicorn main:app --reload
   ```

2. Accede a la documentación interactiva de la API en tu navegador:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints

### 1. `POST /login`

- **Descripción**: Genera un token JWT para autenticarse.
- **Cuerpo de la solicitud**:
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```
- **Respuesta**:
  ```json
  {
    "access_token": "<jwt_token>",
    "token_type": "bearer"
  }
  ```

### 2. `GET /books`

- **Descripción**: Devuelve la lista de libros (requiere JWT).
- **Autenticación**: Enviar el token en el encabezado `Authorization`:
  ```
  Authorization: Bearer <jwt_token>
  ```

### 3. `POST /books`

- **Descripción**: Agrega un libro a la lista (requiere JWT).
- **Cuerpo de la solicitud**:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name"
  }
  ```

### 4. `PUT /books`

- **Descripción**: Actualiza un libro existente por índice (requiere JWT).
- **Cuerpo de la solicitud**:
  ```json
  {
    "index": 0,
    "title": "Updated Title",
    "author": "Updated Author"
  }
  ```

### 5. `DELETE /books`

- **Descripción**: Elimina un libro por índice (requiere JWT).
- **Cuerpo de la solicitud**:
  ```json
  {
    "index": 0
  }
  ```

## Notas

- Los libros se almacenan en un array en memoria, por lo que se perderán al reiniciar el servidor.
- El usuario y contraseña predeterminados para el login son:
  - **Usuario**: `admin`
  - **Contraseña**: `password`