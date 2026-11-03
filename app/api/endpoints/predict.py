from fastapi import APIRouter
from app.schemas.predict import PredictRequest
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("")
async def predict_student(req: PredictRequest):
    result = PredictionService.predict_and_explain(req.features)
    return {
        "success": True,
        "message": "Dự đoán cụm thành công",
        "data": result
    }
