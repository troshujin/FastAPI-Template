from app.user.services.user import UserService
from core.helpers.hashids import decode_single
from fastapi import Request
from sqlalchemy.orm import Session
from core.fastapi.dependencies.permission import BasePermission


def get_user_id_from_path(request):
    hashed_id = request.path_params.get("user_id")
    return decode_single(hashed_id)


class IsAuthenticated(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        del session

        return request.user.id is not None


class IsUserOwner(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        del session
        
        user_id = get_user_id_from_path(request)

        if user_id != request.user.id:
            return False

        return True


class IsAdmin(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService(session).is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        del request, session

        return True
