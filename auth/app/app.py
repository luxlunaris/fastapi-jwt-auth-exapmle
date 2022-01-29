import asyncio

from fastapi import FastAPI

from .config import config
from .db import recreate_db


def create_app() -> FastAPI:
    """Application instance creation"""
    app = FastAPI(title=config.PROJECT_NAME, version="0.1", docs_url="/api")
    recreate_db()
    return app
