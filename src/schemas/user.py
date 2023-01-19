from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class CreateUser(BaseModel):
    username: str


class UpdateUser(BaseModel):
    id: int
    username: str
