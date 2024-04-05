from fastapi import FastAPI

from app.api.v1.endpoints import router as robot_router
from app.api.v1.endpoints.consts import TAGS_METADATA

app = FastAPI(title='GreenAtom Robots API', openapi_tags=TAGS_METADATA)

app.include_router(robot_router)
