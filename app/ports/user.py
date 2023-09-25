from abc import ABC, abstractmethod
from app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: ...

    @abstractmethod
    def get_all(self) -> list[User]: ...

    @abstractmethod
    def get_by_id(self, user_id: str) -> User: ...
