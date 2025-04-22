# Demo FastAPI con SQLModel con relaciones y validaciones

Este proyecto es una demostración de cómo usar **FastAPI** junto con **SQLModel** para construir una API RESTful con relaciones entre modelos, validaciones y documentación automática.

## Tecnologías Usadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construir APIs rápidas y modernas con Python.
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: Biblioteca para trabajar con bases de datos SQL y modelos Pydantic.
- **[SQLite](https://www.sqlite.org/)**: Base de datos ligera para almacenamiento local.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación FastAPI.

## Estructura de Carpetas

```
app/
├── db/
│   ├── database.py       # Configuración de la base de datos y funciones auxiliares
├── models/
│   ├── author.py         # Modelo Author con SQLModel
│   ├── entry.py          # Modelo Entry con SQLModel
├── crud/
│   ├── author.py         # Operaciones CRUD para Author
│   ├── entry.py          # Operaciones CRUD para Entry
├── routes/
│   ├── author.py         # Endpoints relacionados con Author
│   ├── entry.py          # Endpoints relacionados con Entry
├── main.py               # Punto de entrada principal de la aplicación
└── README.md             # Documentación del proyecto
```

## Cómo Ejecutar el Proyecto

1. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el seeder**:
   Si deseas poblar la base de datos con datos iniciales, ejecuta el siguiente comando:
   ```bash
   python seeder.py
   ```
   Esto eliminará las tablas existentes, creará nuevas tablas y añadirá datos de ejemplo.


4. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

5. **Abrir la documentación interactiva**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Explicación del código

### `models/author.py` y `models/entry.py`
- **Author**: Representa un autor con un nombre y un correo único. Tiene una relación con las entradas (`entries`).
- **Entry**: Representa una entrada con un título único y contenido. Está relacionada con un autor.

### `crud/`
- Contiene funciones para realizar operaciones CRUD en la base de datos.
- Ejemplo: `create_author` valida si el correo ya existe antes de crear un nuevo autor.

### `routes/`
- Define los endpoints de la API.
- Ejemplo: `POST /authors` permite crear un autor, validando que el correo sea único.

### `db/database.py`
- Configura la conexión a la base de datos SQLite.
- Proporciona funciones para crear y eliminar tablas.

### `main.py`
- Configura la aplicación FastAPI.
- Incluye rutas y un manejador global de excepciones.

## Documentación de los Endpoints

### **Authors**

- **POST /api/authors**  
  Crear un nuevo autor.  
  **Body**:
  ```json
  {
    "name": "Author Name",
    "email": "author@example.com"
  }
  ```

- **GET /api/authors**  
  Obtener todos los autores.

- **GET /api/authors/{author_id}**  
  Obtener un autor por ID.

- **PUT /api/authors/{author_id}**  
  Actualizar un autor por ID.  
  **Body**:
  ```json
  {
    "name": "Updated Author Name",
    "email": "updated_email@example.com"
  }
  ```

- **DELETE /api/authors/{author_id}**  
  Eliminar un autor por ID.

### **Entries**

- **POST /api/entries**  
  Crear una nueva entrada.  
  **Body**:
  ```json
  {
    "title": "Entry Title",
    "content": "Entry Content",
    "author_name": "Author Name"
  }
  ```

- **GET /api/entries**  
  Obtener todas las entradas.

- **GET /api/entries/{entry_id}**  
  Obtener una entrada por ID.

- **PUT /api/entries/{entry_id}**  
  Actualizar una entrada por ID.  
  **Body**:
  ```json
  {
    "title": "Updated Entry Title",
    "content": "Updated content for the entry"
  }
  ```

- **DELETE /api/entries/{entry_id}**  
  Eliminar una entrada por ID.

## Notas Adicionales

- **Validaciones**:
  - El correo del autor (`email`) debe ser único.
  - El título de la entrada (`title`) debe ser único.
- **Relaciones**:
  - Cada entrada está asociada a un autor.
  - Los endpoints devuelven objetos completos con relaciones cargadas.

---