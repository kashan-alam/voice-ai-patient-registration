from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.patients import router as patients_router
from app.api.vapi import router as vapi_router
from app.core.config import settings
from app.core.exceptions import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.db.database import Base, engine
from app.db.models import Patient


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


# Register centralized exception handlers.
app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler,
)


# Register API routes.
app.include_router(patients_router)
app.include_router(vapi_router)

# Serve dashboard JavaScript and other static files.
dashboard_path = Path(__file__).resolve().parent.parent / "dashboard"

app.mount(
    "/dashboard",
    StaticFiles(directory=dashboard_path),
    name="dashboard",
)


@app.get("/")
def root():
    return {
        "message": "Voice AI Patient Registration System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/dashboard")
def dashboard():
    return FileResponse(
        dashboard_path / "index.html"
    )