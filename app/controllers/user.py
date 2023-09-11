from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.models.user import UserResponse, UserRequest
from app.services.user import UserService
from app.factory.user_data_factory import UserDataFactory
from app.implementations.in_memory_user_repository import InMemoryUserRepository as repository

router = APIRouter()


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add(*, user: UserRequest, user_service: UserService = Depends(repository)):
    to_user = UserDataFactory.to_user(user)
    return user_service.add(to_user)


@router.get('/', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_all(*, user_service: UserService = Depends(repository)):
    return user_service.get_all()
