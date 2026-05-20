from fastapi import APIRouter

from .auth import router as auth_router
from .blog import router as blog_router
from .platform import router as platform_router


routes = APIRouter()
routes.include_router(platform_router)
routes.include_router(auth_router)
routes.include_router(blog_router)
