from fastapi import Query, HTTPException

API_KEY = "ABC123"  # Clave API fake. Debería leerla de un archivo de configuración o variable de entorno o de la base de datos.

def api_key_dependency(api_key: str = Query(..., description="API Key required to access the endpoints")):
    """
    Valida la API KEY proporcionada como parámetro de consulta.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Forbidden",
                "message": "Invalid or missing API KEY",
                "hint": "Ensure you provide a valid 'api_key' query parameter."
            },
        )
