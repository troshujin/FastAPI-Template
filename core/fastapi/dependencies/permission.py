from abc import ABC, abstractmethod
import logging
from typing import List, Type, Union

from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from sqlalchemy.orm import Session

from core.fastapi.dependencies.database import get_db
from core.exceptions.base import UnauthorizedException


class Keyword(ABC):
    pass


class AND(Keyword):
    pass


class OR(Keyword):
    pass


class NOT(Keyword):
    pass


class BasePermission(ABC):
    @abstractmethod
    async def has_permission(self, request: Request, session: Session) -> bool:
        ...


PermList = List[Union[Type[BasePermission], Type[Keyword], List]]


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: PermList):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request, session: Session = Depends(get_db)):
        if not await self.check_permissions(request, session):
            raise UnauthorizedException

    async def check_permissions(self, request: Request, session: Session) -> bool:
        if not self.permissions:
            return False

        if not self.is_valid_perms():
            raise ValueError("Invalid perms.")
        
        invert_next = False
        skip_until_or = False
        has_permission = False

        for perm in self.permissions:
            if isinstance(perm, list):
                if skip_until_or:
                    continue

                has_permission = await self.check_permissions(request, session)
                has_permission = not has_permission if invert_next else has_permission
                invert_next = False
                continue

            if issubclass(perm, Keyword):
                if perm is OR:
                    skip_until_or = False

                    if has_permission:
                        return True
                    continue

                if skip_until_or:
                    continue

                if perm is NOT:
                    invert_next = True
                    continue

                if perm is AND and not has_permission:
                    skip_until_or = True
                    continue

            if skip_until_or:
                continue

            if issubclass(perm, BasePermission):
                has_permission = await perm().has_permission(request, session)
                has_permission = not has_permission if invert_next else has_permission
                invert_next = False
                continue

        return has_permission

    def is_valid_perms(self) -> bool:
        for index, perm in enumerate(self.permissions):
            if isinstance(perm, list):
                if not PermissionDependency.is_valid_perms(perm):
                    return False
                continue

            if issubclass(perm, BasePermission):
                if index == len(self.permissions) - 1:
                    return True

                next_perm = self.permissions[index + 1]
                if isinstance(next_perm, list) or issubclass(next_perm, BasePermission):
                    logging.error(f"TWO PERMISSIONS ADJACENT: {self.permissions}")
                    return False

                if isinstance(next_perm, NOT):
                    logging.error(f"'NOT' AFTER PERMISSON: {self.permissions}")
                    return False

                continue

            if issubclass(perm, Keyword):
                if index == len(self.permissions) - 1:
                    logging.error(f"ENDS ON KEYWORD: {self.permissions}")
                    return False

                if index == 0 and perm is not NOT:
                    logging.error(f"START ON 'AND' or 'OR': {self.permissions}")
                    return False

                if perm is NOT:
                    next_perm = self.permissions[index + 1]
                    if not isinstance(next_perm, list) and not issubclass(
                        next_perm, BasePermission
                    ):
                        logging.error(f"'NOT' LOOKS AT KEYWORD: {self.permissions}")
                        return False

                else:
                    next_perm = self.permissions[index + 1]
                    if next_perm is AND or next_perm is OR:
                        logging.error(f"'AND' or 'OR' LOOKS AT 'AND' or 'OR': {self.permissions}")
                        return False
                continue

        return True
