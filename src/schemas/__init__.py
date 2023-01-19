from pydantic import BaseModel
from typing import Optional


class Default(BaseModel):
    message: Optional[str]
    error: Optional[str]

    class Config:
        orm_mode: True


from .item import *
from .user import *
