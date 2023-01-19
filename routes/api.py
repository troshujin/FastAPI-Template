from fastapi import APIRouter
from src.endpoints import (
    item,
    user,
)

router = APIRouter(prefix="/api")

router.include_router(item.router)
router.include_router(user.router)
