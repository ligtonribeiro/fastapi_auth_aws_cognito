from app.models.user import User
from app.ports.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def add(self, user: User) -> User:
        return self.user_repository.add(user)

    def get_all(self) -> list[User]:
        return self.user_repository.get_all()

    def get_by_id(self, user_id) -> User:
        return self.user_repository.get_by_id(user_id)
