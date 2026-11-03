from fastapi import APIRouter
from app.schemas.clustering import KMeansTrainRequest
from app.services.kmeans_service import KMeansService

router = APIRouter(prefix="/clustering", tags=["Clustering"])

@router.post("/train")
async def train_kmeans(req: KMeansTrainRequest):
    result = KMeansService.train_and_visualize(
        file_id=req.file_id,
        feature_columns=req.feature_columns,
        n_clusters=req.n_clusters,
        scaling_method=req.scaling_method
    )
    return {
        "success": True,
        "message": f"Phân cụm K-Means thành công với K={req.n_clusters}",
        "data": result
    }
