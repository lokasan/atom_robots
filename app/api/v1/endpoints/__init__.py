from fastapi import APIRouter

from .robot_api import router as robot_router

router = APIRouter()
router.include_router(robot_router)
