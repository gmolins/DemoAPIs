from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uvicorn

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Crear (Subir un fichero)
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    This endpoint uploads files :) test
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

# Leer (Descargar un fichero)
@app.get("/files/{file_name}")
async def read_file(file_name: str):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# Obtener la lista de todos los ficheros
@app.get("/files/")
async def list_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

# Actualizar (Reemplazar un fichero)
@app.put("/files/{file_name}")
async def update_file(file_name: str, file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"message": f"File '{file_name}' updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")

# Eliminar (Borrar un fichero)
@app.delete("/files/{file_name}")
async def delete_file(file_name: str):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        os.remove(file_path)
        return {"message": f"File '{file_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)