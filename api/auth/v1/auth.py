"""User endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas.jwt import RefreshTokenSchema, TokensSchema
from app.auth.services.auth import AuthService
from app.auth.schemas.auth import LoginSchema
from core.fastapi.dependencies.permission import AllowAll, PermissionDependency
from core.fastapi.dependencies.database import get_db
from core.versioning import version


auth_v1_router = APIRouter()


@auth_v1_router.post(
    "/login",
    response_model=TokensSchema,
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def login(schema: LoginSchema, session: Session = Depends(get_db)):
    return await AuthService(session).login(schema)


@auth_v1_router.post(
    "/refresh",
    response_model=TokensSchema,
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def refresh(schema: RefreshTokenSchema, session: Session = Depends(get_db)):
    return await AuthService(session).refresh(schema)
# This is the future code in wich we send the refresh token as a cookie, but due to certain circumstances 
# we will send the refresh tokens in the body
# @version(1) 
# async def refresh(response: Response, schema: RefreshTokenSchema, session: Session = Depends(get_db)):
#     refresh_token = await AuthService(session).refresh(schema)
#     response.set_cookie(key='refresh_token', value={refresh_token}, httponly=True)
#     return True