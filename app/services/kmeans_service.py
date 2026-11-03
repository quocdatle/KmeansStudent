from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from app.core.exceptions import AppException
from app.services.data_service import DataService

class KMeansService:
    # Lưu trữ model và scaler hiện tại trong bộ nhớ phục vụ inference
    current_model: KMeans = None
    current_scaler: Any = None
    current_features: List[str] = []
    current_profiles: List[Dict[str, Any]] = []

    @staticmethod
    def get_scaler(scaling_method: str):
        if scaling_method == "minmax":
            return MinMaxScaler()
        return StandardScaler()

    @staticmethod
    def prepare_data(df: pd.DataFrame, feature_columns: List[str], scaling_method: str = "standard") -> Tuple[np.ndarray, Any, pd.DataFrame]:
        for col in feature_columns:
            if col not in df.columns:
                raise AppException(f"Cột đặc trưng '{col}' không tồn tại trong dataset")
        
        # Lấy dữ liệu và xử lý missing cơ bản
        clean_df = df[feature_columns].dropna()
        if len(clean_df) < 5:
            raise AppException("Dữ liệu sau khi loại bỏ giá trị trống quá ít để huấn luyện (tối thiểu 5 dòng).")

        scaler = KMeansService.get_scaler(scaling_method)
        scaled_data = scaler.fit_transform(clean_df)
        return scaled_data, scaler, clean_df

    @staticmethod
    def calculate_elbow_and_silhouette(
        file_id: str,
        feature_columns: List[str],
        max_k: int = 10,
        scaling_method: str = "standard"
    ) -> Dict[str, Any]:
        df = DataService.load_dataframe(file_id)
        scaled_data, _, _ = KMeansService.prepare_data(df, feature_columns, scaling_method)

        max_k = min(max_k, len(scaled_data) - 1)
        k_values = list(range(2, max_k + 1))
        inertias = []
        silhouettes = []

        for k in k_values:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(scaled_data)
            inertias.append(float(km.inertia_))
            sil = float(silhouette_score(scaled_data, labels))
            silhouettes.append(sil)

        best_k = k_values[int(np.argmax(silhouettes))]

        return {
            "k_values": k_values,
            "inertias": inertias,
            "silhouette_scores": silhouettes,
            "recommended_k": best_k
        }

    @staticmethod
    def train_and_visualize(
        file_id: str,
        feature_columns: List[str],
        n_clusters: int = 3,
        scaling_method: str = "standard"
    ) -> Dict[str, Any]:
        df = DataService.load_dataframe(file_id)
        scaled_data, scaler, clean_df = KMeansService.prepare_data(df, feature_columns, scaling_method)

        if n_clusters >= len(scaled_data):
            raise AppException("Số cụm K phải nhỏ hơn số lượng mẫu dữ liệu.")

        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(scaled_data)
        sil_avg = float(silhouette_score(scaled_data, labels))

        # Lưu trạng thái model phục vụ suy luận
        KMeansService.current_model = km
        KMeansService.current_scaler = scaler
        KMeansService.current_features = feature_columns

        # Giảm chiều PCA 2D
        pca = PCA(n_components=2, random_state=42)
        pca_2d = pca.fit_transform(scaled_data)
        centroids_2d = pca.transform(km.cluster_centers_)

        id_col = "student_id" if "student_id" in df.columns else None

        pca_points = []
        for i, (p, label) in enumerate(zip(pca_2d, labels)):
            orig_idx = clean_df.index[i]
            pt_id = str(df.loc[orig_idx, id_col]) if id_col else f"Mẫu #{i+1}"
            pca_points.append({
                "id": pt_id,
                "pc1": round(float(p[0]), 4),
                "pc2": round(float(p[1]), 4),
                "cluster": int(label)
            })

        pca_centroids = [
            {"cluster": c_idx, "pc1": round(float(c[0]), 4), "pc2": round(float(c[1]), 4)}
            for c_idx, c in enumerate(centroids_2d)
        ]

        # Profile từng cụm
        clean_df_with_label = clean_df.copy()
        clean_df_with_label["cluster"] = labels

        profiles = []
        total_len = len(clean_df)

        for c in range(n_clusters):
            c_data = clean_df_with_label[clean_df_with_label["cluster"] == c]
            count = len(c_data)
            percentage = round((count / total_len) * 100, 2)
            means = c_data[feature_columns].mean().round(2).to_dict()

            # Tự động gán nhãn mô tả sơ bộ
            label_text = f"Cụm {c}"

            profiles.append({
                "cluster": c,
                "count": count,
                "percentage": percentage,
                "label": label_text,
                "feature_means": means
            })

        KMeansService.current_profiles = profiles

        return {
            "n_clusters": n_clusters,
            "silhouette_avg": round(sil_avg, 4),
            "pca_data": pca_points,
            "pca_centroids": pca_centroids,
            "explained_variance_ratio": [round(float(v), 4) for v in pca.explained_variance_ratio_],
            "profiles": profiles
        }
