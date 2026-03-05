from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router
from .routers import tags as tags_router

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Check if React build exists
REACT_DIST = Path("frontend/dist")
USE_REACT = REACT_DIST.exists() and (REACT_DIST / "index.html").exists()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()
    yield


app = FastAPI(title="Modern Software Dev Starter (Week 5)", lifespan=lifespan)


# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Convert HTTPException to envelope format."""
    error_codes = {
        400: "BAD_REQUEST",
        404: "NOT_FOUND",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_ERROR",
    }
    code = error_codes.get(exc.status_code, "ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "data": None,
            "error": {"code": code, "message": exc.detail},
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "data": None,
            "error": {"code": "INTERNAL_ERROR", "message": str(exc)},
        },
    )


# Mount static files
if USE_REACT:
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
else:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def root() -> FileResponse:
    if USE_REACT:
        return FileResponse("frontend/dist/index.html")
    return FileResponse("frontend/index.html")


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)
app.include_router(tags_router.router)
