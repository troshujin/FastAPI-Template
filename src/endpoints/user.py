from fastapi import APIRouter, Depends, Response, Request
import src.schemas as schem
from src.services.user import UserService
from database import get_db
import database.model_enums as me

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[schem.User])
def get_users(session=Depends(get_db), skip: int = None, limit: int = None, is_locked: bool = None):
    return UserService(session).get_users(skip, limit, is_locked)


@router.post("", response_model=schem.User)
def create_user(user: schem.CreateUser, session=Depends(get_db)):
    return UserService(session).create_user(user)


@router.patch("", response_model=schem.User)
def update_user(user: schem.UpdateUser, session=Depends(get_db)):
    return UserService(session).update_user(user)


@router.get("/{id}", response_model=schem.User)
def get_user(id: str, session=Depends(get_db)):
    return UserService(session).get_user(id)


@router.delete("/{id}")
def delete_user(id: str, session=Depends(get_db)):
    return UserService(session).delete_user(id)
