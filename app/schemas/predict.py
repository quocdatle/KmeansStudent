from typing import Dict, Any, List
from pydantic import BaseModel

class PredictRequest(BaseModel):
    features: Dict[str, float]

class PredictResponse(BaseModel):
    assigned_cluster: int
    cluster_label: str
    distances_to_centroids: Dict[str, float]
    explanation: str
    comparison_with_cluster_mean: Dict[str, Dict[str, float]]
