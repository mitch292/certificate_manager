from fastapi import APIRouter

from app.api.routes import users, certificates, webhooks

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(certificates.router, tags=['certificates'])
api_router.include_router(webhooks.router, tags=['webhooks'])
