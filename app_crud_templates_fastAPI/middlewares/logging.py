import time
from fastapi import Request

async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Leer el cuerpo de la solicitud si es POST o PUT
    if request.method in ["POST", "PUT"]:
        body = await request.body()
        print(f"Request Body: {body.decode('utf-8')}")
    
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} - Processed in {process_time:.4f}s")
    return response
