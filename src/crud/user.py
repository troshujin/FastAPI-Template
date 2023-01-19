from fastapi import HTTPException
from src.services import AppCRUD
from database.models import User
from sqlalchemy import select, update, delete, insert, and_


class UserCRUD(AppCRUD):
    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user(self, id: str) -> User:
        stmt = select(User).where(User.id == id)
        return self.session.execute(stmt).scalars().first()
    
    def get_users(self, skip: int = None, limit: int = None, is_locked: bool = None) -> list[User]:
        stmt = select(User)

        if is_locked is not None:
            stmt = stmt.where(User.is_locked == is_locked)

        stmt = stmt.offset(skip).limit(limit)
        return self.session.execute(stmt).scalars().all()
    
    def update_user(self, updated_user: User) -> User:
        user = self.get_user(updated_user.id)
        if not user: raise HTTPException(status_code=404, detail="User not found.")

        stmt = update(User).where(User.id == updated_user.id).values(
            avatar=updated_user.avatar,
            banner=updated_user.banner,
            banner_color=updated_user.banner_color,
            discord_tag=updated_user.discord_tag,
            is_locked=updated_user.is_locked,
        ).returning(User)

        self.session.execute(stmt)
        self.session.commit()

        return self.get_user(updated_user.id)
    
    def delete_user(self, id: str) -> int:
        rows_deleted = self.session.query(User).filter(User.id == id).delete()
        self.session.commit()
        return rows_deleted
