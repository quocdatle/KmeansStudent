from typing import Dict, Any
import numpy as np
import pandas as pd
from app.core.exceptions import AppException
from app.services.kmeans_service import KMeansService

class PredictionService:
    @staticmethod
    def predict_and_explain(features: Dict[str, float]) -> Dict[str, Any]:
        if KMeansService.current_model is None or KMeansService.current_scaler is None:
            raise AppException("Mô hình K-Means chưa được huấn luyện. Vui lòng chạy phân cụm trước.", status_code=400)

        required_features = KMeansService.current_features
        for feat in required_features:
            if feat not in features:
                raise AppException(f"Thiếu thông tin đặc trưng: {feat}", status_code=400)

        # Tạo DataFrame đặc trưng theo đúng thứ tự cột để tránh warning của scikit-learn
        feature_df = pd.DataFrame([[features[feat] for feat in required_features]], columns=required_features)
        scaled_vector = KMeansService.current_scaler.transform(feature_df)

        # Tính khoảng cách đến các tâm cụm
        centroids = KMeansService.current_model.cluster_centers_
        distances = np.linalg.norm(centroids - scaled_vector, axis=1)

        assigned_cluster = int(np.argmin(distances))
        dist_dict = {f"Cụm {i}": round(float(d), 4) for i, d in enumerate(distances)}

        # Lấy profile của cụm được gán
        target_profile = next((p for p in KMeansService.current_profiles if p["cluster"] == assigned_cluster), None)
        cluster_label = target_profile["label"] if target_profile else f"Cụm {assigned_cluster}"

        # So sánh đặc trưng của sinh viên với trung bình của cụm
        comparison = {}
        explanation_parts = []
        if target_profile:
            means = target_profile["feature_means"]
            for feat in required_features:
                val = features[feat]
                m_val = means.get(feat, 0)
                diff = round(val - m_val, 2)
                comparison[feat] = {
                    "student_value": val,
                    "cluster_mean": m_val,
                    "difference": diff
                }
                if abs(diff) <= 0.15 * (m_val if m_val != 0 else 1):
                    explanation_parts.append(f"{feat} ({val}) rất sát với mức trung bình của cụm ({m_val})")

        expl_text = f"Sinh viên được xếp vào {cluster_label} do khoảng cách đến tâm cụm này là ngắn nhất ({dist_dict[f'Cụm {assigned_cluster}']}). "
        if explanation_parts:
            expl_text += "Các đặc trưng tương đồng nổi bật: " + "; ".join(explanation_parts) + "."

        return {
            "assigned_cluster": assigned_cluster,
            "cluster_label": cluster_label,
            "distances_to_centroids": dist_dict,
            "explanation": expl_text,
            "comparison_with_cluster_mean": comparison
        }
