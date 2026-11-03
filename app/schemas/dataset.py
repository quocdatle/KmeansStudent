from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DatasetPreviewResponse(BaseModel):
    filename: str
    total_rows: int
    total_columns: int
    columns: List[str]
    numeric_columns: List[str]
    missing_values: Dict[str, int]
    sample_data: List[Dict[str, Any]]

class PreprocessRequest(BaseModel):
    file_id: str
    feature_columns: List[str]
    missing_strategy: str = "drop"  # "drop", "impute_mean", "impute_median"
    scaling_method: str = "standard"  # "standard", "minmax"
