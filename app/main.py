from fastapi import FastAPI

from app.core.config import APP_NAME
from app.api import api_router

app = FastAPI(title=APP_NAME)

app.include_router(api_router)