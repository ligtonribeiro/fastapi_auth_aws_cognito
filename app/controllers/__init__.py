from fastapi import APIRouter, Depends

from .user import router as user_router

from app.shared.auth import AuthenticatedUser

main_router = APIRouter()

main_router.include_router(user_router, prefix='/user', tags=['User'])
