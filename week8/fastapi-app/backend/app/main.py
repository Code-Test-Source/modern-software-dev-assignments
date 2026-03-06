from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import Base, engine
from .routers import action_items, notes

_FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Developer Control Center", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(action_items.router)

app.mount("/static", StaticFiles(directory=str(_FRONTEND_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(str(_FRONTEND_DIR / "index.html"))
