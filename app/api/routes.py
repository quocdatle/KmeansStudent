from fastapi import APIRouter
from app.api.endpoints import dataset, analysis, clustering, predict

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(dataset.router)
api_router.include_router(analysis.router)
api_router.include_router(clustering.router)
api_router.include_router(predict.router)
