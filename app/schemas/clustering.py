from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ElbowRequest(BaseModel):
    file_id: str
    feature_columns: List[str]
    max_k: int = Field(default=10, ge=3, le=15)
    scaling_method: str = "standard"

class ElbowResponse(BaseModel):
    k_values: List[int]
    inertias: List[float]
    silhouette_scores: List[float]
    recommended_k: int

class KMeansTrainRequest(BaseModel):
    file_id: str
    feature_columns: List[str]
    n_clusters: int = Field(default=3, ge=2, le=10)
    scaling_method: str = "standard"

class PCAPoint(BaseModel):
    id: Optional[str] = None
    pc1: float
    pc2: float
    cluster: int

class CentroidPoint(BaseModel):
    cluster: int
    pc1: float
    pc2: float

class ClusterProfile(BaseModel):
    cluster: int
    count: int
    percentage: float
    label: str
    feature_means: Dict[str, float]

class KMeansTrainResponse(BaseModel):
    n_clusters: int
    silhouette_avg: float
    pca_data: List[PCAPoint]
    pca_centroids: List[CentroidPoint]
    explained_variance_ratio: List[float]
    profiles: List[ClusterProfile]
