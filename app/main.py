from fastapi import FastAPI

from app.api import api_router
from app.settings import APP_NAME

app = FastAPI(title=APP_NAME)

app.include_router(api_router)
