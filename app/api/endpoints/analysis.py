from fastapi import APIRouter
from app.schemas.clustering import ElbowRequest
from app.services.kmeans_service import KMeansService

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/elbow")
async def calculate_elbow(req: ElbowRequest):
    result = KMeansService.calculate_elbow_and_silhouette(
        file_id=req.file_id,
        feature_columns=req.feature_columns,
        max_k=req.max_k,
        scaling_method=req.scaling_method
    )
    return {"success": True, "data": result}
