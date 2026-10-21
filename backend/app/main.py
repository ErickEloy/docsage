from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import upload, ask, health


def create_app() -> FastAPI:
    app = FastAPI(
        title="Docsage API",
        description="RAG API for PDF Q&A",
        version="0.1.0",
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(upload.router, prefix="/api", tags=["upload"])
    app.include_router(ask.router, prefix="/api", tags=["ask"])

    return app


app = create_app()