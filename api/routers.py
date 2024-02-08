from fastapi import APIRouter

from api import google_drive


api_router = APIRouter()
api_router.include_router(google_drive.router)
