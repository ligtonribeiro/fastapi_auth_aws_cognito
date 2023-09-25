from fastapi import APIRouter, Depends, status

from app.models.user import UserResponse, UserRequest
from app.services.user import UserService
from app.factory.user_data_factory import UserDataFactory
from app.adapters.repository.in_memory.user_repository_impl import InMemoryUserRepository

adapter = InMemoryUserRepository()
service = UserService(adapter)

router = APIRouter()


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add(*, user: UserRequest, user_service: UserService = Depends(lambda: service)):
    to_user = UserDataFactory.to_user(user)
    return user_service.add(to_user)


@router.get('/', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_all(*, user_service: UserService = Depends(lambda: service)):
    return user_service.get_all()
