import uuid

from app.models.user import User
from app.repository.user import UserRepository

data = []


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._id = uuid.uuid4()

    def add(self, user: User) -> User:
        user.id = self._id
        data.append(user)
        return user

    def get_all(self) -> list[User]:
        return data

    def get_by_id(self, user_id: str) -> User:
        return self.data.get(user_id)
