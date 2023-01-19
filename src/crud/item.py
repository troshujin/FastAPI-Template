from fastapi import HTTPException
from src.services import AppCRUD
from database.models import Item, User
from sqlalchemy import select, update, delete, insert, and_


class ItemCRUD(AppCRUD):
    def create_item(self, user: User, item: Item) -> Item:
        item.created_by = user.id
        item.updated_by = user.id

        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_item(self, id: int) -> Item:
        stmt = select(Item).where(Item.id == id)
        return self.session.execute(stmt).scalars().first()

    def get_items(self, skip, limit, is_hidden) -> list[Item]:
        stmt = select(Item)
        if is_hidden is not None:
            stmt = stmt.where(Item.is_hidden == is_hidden)
        stmt = stmt.offset(skip).limit(limit)
        return self.session.execute(stmt).scalars().all()

    def update_item(self, user: User, updated_item: Item) -> Item:

        item = self.get_item(updated_item.id)
        if not item: raise HTTPException(status_code=404, detail="Item not found.")

        stmt = update(Item).where(Item.id == updated_item.id).values(
            name=updated_item.name,
            description=updated_item.description,
            is_hidden=updated_item.is_hidden,
            price=updated_item.price,
            updated_by = user.id
        ).returning(Item)

        self.session.execute(stmt)
        self.session.commit()

        return self.get_item(updated_item.id)

    def delete_item(self, id: int) -> int:
        rows_deleted = self.session.query(Item).filter(Item.id == id).delete()
        if not rows_deleted:
            raise HTTPException(status_code=404, detail="Item not found.")
            
        self.session.commit()
        return rows_deleted

    def add_view(self, item):
        item.view_count += 1
        self.session.commit()
        self.session.refresh(item)
        return item
