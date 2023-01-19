from fastapi import APIRouter, Depends, Response, Request
import src.schemas as schem
from src.services.item import ItemService
from database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[schem.Item])
def get_items(
    session=Depends(get_db),
    skip: int = None,
    limit: int = None,
    is_hidden: bool = None,
    search: str = None,
):
    return ItemService(session).get_items(skip, limit, is_hidden, search)


@router.post("", response_model=schem.Item)
def create_item(item: schem.CreateItem, session=Depends(get_db)):
    return ItemService(session).create_item(item)


@router.patch("", response_model=schem.Item)
def update_item(item: schem.UpdateItem, session=Depends(get_db)):
    return ItemService(session).update_item(item)


@router.get("/{id}", response_model=schem.Item)
def get_item(id: int, session=Depends(get_db), add_view: bool = True):
    item = ItemService(session).get_item(id, add_view)
    if item.is_hidden is not None:
        ...
        # You could do an authorization check here :D
    
    return item


@router.delete("/{id}")
def delete_item(id: int, session=Depends(get_db)):
    return ItemService(session).delete_item(id)
