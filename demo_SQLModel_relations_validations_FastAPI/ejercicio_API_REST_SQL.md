![The Bridge](../../assets/python.jpg)

----------

# Ejercicios de Mejora para el Proyecto FastAPI con SQLModel

A continuación, se presentan ejercicios diseñados para mejorar el proyecto de FastAPI con SQLModel


## Ejercicio 1: **Añadir un modelo y endpoints para Categorías**

### Descripción
Crear un nuevo modelo `Category` que permita clasificar las entradas (`Entry`) en categorías. Cada entrada puede pertenecer a una categoría.

### Tareas
1. Crear el modelo `Category` en `models/category.py`.
2. Añadir relaciones entre `Entry` y `Category`.
3. Crear funciones CRUD para `Category` en `crud/category.py`.
4. Crear endpoints para `Category` en `routes/category.py`.
5. Actualizar el archivo `main.py` para incluir las rutas de categorías.

### Puntos clave
- Validar que el nombre de la categoría sea único.
- Permitir listar todas las entradas de una categoría.

---

## Ejercicio 2: **Añadir un sistema de logs**

### Descripción
Implementar un sistema de logs para registrar las operaciones realizadas en la API.

### Tareas
1. Configurar un logger en `main.py`.
2. Registrar las solicitudes y respuestas en los endpoints.
3. Registrar errores en un archivo de logs.

### Puntos clave
- Usar la biblioteca `logging` de Python.
- Configurar diferentes niveles de logs (INFO, ERROR, etc.).


---

## Ejercicio 3: **Validación de datos más robusta**
- **Problema**: Actualmente, las validaciones de los datos dependen principalmente de los modelos de entrada (`EntryCreate`, `AuthorCreate`), pero no se realizan validaciones adicionales en los endpoints.
- **Propuesta**:
  - Validar que los campos `title` y `email` no estén vacíos antes de procesar las solicitudes.
  - Asegurarse de que los datos enviados en los endpoints de actualización (`PUT`) no sobrescriban valores críticos como `id`.

---

## Ejercicio 4: **Manejo de errores más detallado**
- **Problema**: Los mensajes de error en los endpoints son genéricos y no siempre informativos.
- **Propuesta**:
  - Personalizar los mensajes de error para que sean más específicos.
  - Usar un manejador de excepciones global para capturar errores comunes como `IntegrityError` de SQLAlchemy.

---

## Ejercicio 5: **Añadir soporte para Soft Deletes**
- **Problema**: Actualmente, las entradas y autores se eliminan permanentemente de la base de datos.
- **Propuesta**:
  - Añadir un campo `is_deleted` a los modelos `Author` y `Entry`.
  - Modificar las funciones CRUD para filtrar los registros eliminados.
  - Cambiar los endpoints de eliminación para que marquen los registros como eliminados en lugar de borrarlos.

---

## Ejercicio 6: **Optimización de consultas**
- **Problema**: Algunas consultas, como `get_entries_by_author_name`, pueden ser ineficientes si la base de datos crece.
- **Propuesta**:
  - Usar `join` en las consultas para reducir el número de operaciones en la base de datos.
  - Añadir índices adicionales en campos como `author_name` y `title`.

---

## Ejercicio 7: **Añadir soporte para ordenación**
- **Problema**: Los endpoints de lectura no permiten ordenar los resultados.
- **Propuesta**:
  - Añadir un parámetro opcional `order_by` a los endpoints de lectura.
  - Permitir ordenar por campos como `title`, `created_at`, etc.

---

## Ejercicio 8: **Añadir timestamps a los modelos**
- **Problema**: No hay forma de saber cuándo se crearon o actualizaron los registros.
- **Propuesta**:
  - Añadir campos `created_at` y `updated_at` a los modelos `Author` y `Entry`.
  - Usar `default` y `onupdate` en los campos para que se actualicen automáticamente.

---

## Ejercicio 9: **Documentación más detallada**
- **Problema**: La documentación generada automáticamente no incluye descripciones detalladas de los endpoints.
- **Propuesta**:
  - Usar el parámetro `description` en los decoradores de los endpoints para añadir descripciones.
  - Añadir ejemplos más detallados en los modelos de entrada.

---

## Ejercicio 10: **Añadir soporte para búsqueda avanzada**
- **Problema**: No hay un endpoint para buscar entradas por múltiples criterios.
- **Propuesta**:
  - Crear un endpoint `GET /api/entries/search`.
  - Permitir buscar por título, contenido, autor, etc.
  - Usar filtros dinámicos en las consultas SQL.

---

## Ejercicio 11: **Añadir paginación a los endpoints de lectura**

### Descripción
Modificar los endpoints de lectura (`GET`) para soportar paginación.

### Tareas
1. Añadir parámetros `limit` y `offset` a los endpoints de lectura en `routes/author.py` y `routes/entry.py`.
2. Modificar las funciones CRUD para aplicar paginación.

### Puntos clave
- Usar `limit` para definir el número máximo de resultados.
- Usar `offset` para definir desde qué posición empezar a leer.

---