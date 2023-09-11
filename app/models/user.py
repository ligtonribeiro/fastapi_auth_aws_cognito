from typing import Optional, Any
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[Any]
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
