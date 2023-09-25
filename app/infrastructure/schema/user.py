from uuid import UUID, uuid4
from datetime import datetime

from pydantic import Field
from beanie import Document

from app.models.user import User


class UserSchema(Document, User):
    id: UUID = Field(default_factory=uuid4)
    date: datetime = datetime.now()

    class Settings:
        name = 'users'
