"""Home endpoints."""

from app.permission import AllowAll
from fastapi import APIRouter, Depends, Response
from core.fastapi.dependencies.permission import PermissionDependency
from core.versioning import version


home_v1_router = APIRouter()


@home_v1_router.get(
    "/health",
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
@version(1)
async def health():
    return Response(status_code=200)
