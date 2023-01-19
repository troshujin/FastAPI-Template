# from src.services import AppCRUD
# from database.models import X
# from sqlalchemy import select, update, delete, insert, and_


# class XCRUD(AppCRUD):
#     def create_x_(self, x_: X) -> X:
#         self.session.add(x_)
#         self.session.commit()
#         return x_

#     def get_x_(self, id: int) -> X:
#         stmt = select(X).where(X.id == id)
#         return self.session.execute(stmt).scalars().first()
    
#     def get_x_s(self, skip, limit) -> list[X]:
#         stmt = select(X).offset(skip).limit(limit)
#         return self.session.execute(stmt).scalars().all()
    
#     def update_x_(self, updated_x_: X) -> X:
#         x_ = XCRUD(self.session).get_user(updated_x_.id)
#         x_.y = x_.y if updated_x_.y is not None else updated_x_.y
        
    
#     def delete_x_(self, id: int) -> int:
#         rows_deleted = self.session.query(X).filter(X.id == id).delete()
#         self.session.commit()
#         return rows_deleted

from .item import ItemCRUD
from .user import UserCRUD
