from datetime import datetime
from pydantic import BaseModel


class CreateItem(BaseModel):
    name: str
    description: str = None
    price: int = None
    is_hidden: bool = False


class Item(BaseModel):
    id: int
    description: str = None
    name: str
    price: int = None
    is_hidden: bool
    view_count: int

    created_by: int
    created_on: datetime
    updated_by: int
    updated_on: datetime
    

class UpdateItem(BaseModel):
    id: int
    name: str
    description: str = None
    price: int = None
    is_hidden: bool = False
