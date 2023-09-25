from typing import Optional, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str
    password: str


class UserRequest(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: Any
    name: str
    email: str
