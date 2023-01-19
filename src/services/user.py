from fastapi import HTTPException
from src.services import AppService
import src.crud as crud
import database.models as mo
import src.schemas as schem


class UserService(AppService):
    def get_users(self, skip: int = None, limit: int = None, is_locked: bool = None) -> list[schem.User]:
        users: list[mo.User] = crud.UserCRUD(self.session).get_users(skip, limit, is_locked)
        
        return [schem.User(**user.__dict__)for user in users]

    def create_user(self, user: schem.CreateUser) -> schem.User:
        new_user = crud.UserCRUD(self.session).create_user(
            user=mo.User(username=user.username)
        )

        return schem.User(**new_user.__dict__)

    def update_user(self, user: schem.UpdateUser) -> schem.User:
        updated_user = crud.UserCRUD(self.session).update_user(user)

        return schem.User(**updated_user.__dict__)

    def get_user(self, id: str = None) -> schem.User:
        user = crud.UserCRUD(self.session).get_user(id)
        if not user: raise HTTPException(status_code=404, detail="User not found.")

        return schem.User(**user.__dict__)

    def delete_user(self, id: str = None):
        rows_deleted = crud.UserCRUD(self.session).delete_user(id)
        return {"message": f"Succesfully deleted {rows_deleted} user(s)."}