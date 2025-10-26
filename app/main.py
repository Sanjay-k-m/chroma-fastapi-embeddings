from typing import Dict
from fastapi import FastAPI, status, Request            
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import generic_exception_handler, validation_exception_handler
from app.routes import notes_route

app = FastAPI(
    title="chroma-fastapi-embeddings",
    description="API to manage notes with embeddings",
    version="1",
    openapi_tags=[
        {"name": "notes", "description": "Notes CRUD operations"},
        {"name": "system", "description": "System and health endpoints"},
    ],
)

# Register global error handlers
@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    return await validation_exception_handler(request, exc)

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return await generic_exception_handler(request, exc)

# Routes
app.include_router(notes_route, prefix="/notes", tags=["notes"])

@app.get("/", tags=["system"], status_code=status.HTTP_200_OK)
async def root():
    return {"status": "Server is Running"}

@app.get("/health", tags=["system"], status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
