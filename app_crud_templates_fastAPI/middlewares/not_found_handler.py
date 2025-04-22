from fastapi import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class NotFoundHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api"):
            try:
                response = await call_next(request)
                if response.status_code == 404:
                    return JSONResponse(
                        content={
                            "error": "Not Found",
                            "message": "The requested resource was not found.",
                            "hint": "Check the URL or contact support if the issue persists."
                        },
                        status_code=404
                    )
                return response
            except Exception as exc:
                return JSONResponse(
                    content={"error": "Internal Server Error", "message": str(exc)},
                    status_code=500
                )
        # Si la ruta no comienza con /api/items, pasa la solicitud sin modificar
        return await call_next(request)
