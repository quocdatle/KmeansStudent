import sys
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thêm thư mục gốc dự án vào PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.data_service import DataService
from app.services.kmeans_service import KMeansService
from app.services.prediction_service import PredictionService

def test_data_service_preview():
    preview = DataService.preview_dataset("student_sample.csv")
    assert preview["total_rows"] > 0
    assert "student_id" in preview["columns"]
    assert "study_hours_per_week" in preview["numeric_columns"]
    print("  [PASSED] test_data_service_preview")

def test_elbow_and_silhouette():
    features = ["study_hours_per_week", "attendance_rate", "midterm_score", "final_score"]
    result = KMeansService.calculate_elbow_and_silhouette("student_sample.csv", features, max_k=5)
    assert len(result["k_values"]) == 4
    assert len(result["inertias"]) == 4
    assert len(result["silhouette_scores"]) == 4
    assert result["recommended_k"] in [2, 3, 4, 5]
    print("  [PASSED] test_elbow_and_silhouette")

def test_kmeans_train_and_predict():
    features = ["study_hours_per_week", "attendance_rate", "midterm_score", "final_score"]
    train_res = KMeansService.train_and_visualize("student_sample.csv", features, n_clusters=3)
    assert train_res["n_clusters"] == 3
    assert len(train_res["pca_data"]) > 0
    assert len(train_res["pca_centroids"]) == 3
    assert len(train_res["profiles"]) == 3

    # Test inference
    sample_student = {
        "study_hours_per_week": 24.0,
        "attendance_rate": 96.0,
        "midterm_score": 90.0,
        "final_score": 92.0
    }
    pred_res = PredictionService.predict_and_explain(sample_student)
    assert "assigned_cluster" in pred_res
    assert pred_res["assigned_cluster"] in [0, 1, 2]
    assert "explanation" in pred_res
    print("  [PASSED] test_kmeans_train_and_predict")

if __name__ == "__main__":
    print("Starting system test...")
    test_data_service_preview()
    test_elbow_and_silhouette()
    test_kmeans_train_and_predict()
    print(">>> ALL MODULES PASSED SUCCESSFULLY!")
