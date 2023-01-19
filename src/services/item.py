from fastapi import HTTPException
from src.services import AppService
import src.crud as crud
import database.models as mo
import src.schemas as schem


class ItemService(AppService):
    def get_items(self, skip: int = None, limit: int = None, is_hidden: bool = None, search: str = None) -> list[schem.Item]:
        items: list[mo.Item] = crud.ItemCRUD(self.session).get_items(skip, limit, is_hidden)

        if search is not None:
            items = filter(
                lambda item: search.upper() in item.name.upper()
                or (item.description is not None and search.upper() in item.description.upper()),
                items
            )
        
        return [schem.Item(**item.__dict__) for item in items]

    def create_item(self, item: schem.CreateItem) -> schem.Item:

        # Do epic auth stuff to get the user or something
        user = crud.UserCRUD(self.session).get_user(1)
        
        new_item = crud.ItemCRUD(self.session).create_item(
            user, 
            item=mo.Item(**item.__dict__)
        )
        return schem.Item(**new_item.__dict__)

    def update_item(self, item: schem.UpdateItem) -> schem.Item:

        # Do epic auth stuff to get the user or something
        user = crud.UserCRUD(self.session).get_user(1)

        updated_item = crud.ItemCRUD(self.session).update_item(user, item)

        return schem.Item(**updated_item.__dict__)

    def get_item(self, id: int = None, add_view: bool = True) -> schem.Item:
        item = crud.ItemCRUD(self.session).get_item(id)
        if not item: raise HTTPException(status_code=404, detail="Item not found.")
        
        if add_view: item = crud.ItemCRUD(self.session).add_view(item)
        
        return schem.Item(**item.__dict__)

    def delete_item(self, id: int = None):
        rows_deleted = crud.ItemCRUD(self.session).delete_item(id)
        return {"message": f"Succesfully deleted {rows_deleted} item(s)."}