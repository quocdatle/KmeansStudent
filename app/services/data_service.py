from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
from app.core.config import SAMPLE_DIR, UPLOAD_DIR
from app.core.exceptions import AppException

class DataService:
    @staticmethod
    def get_file_path(file_id: str) -> Path:
        """Tìm đường dẫn file dựa vào file_id (ưu tiên sample hoặc upload)."""
        if file_id == "sample" or file_id == "student_sample.csv":
            sample_path = SAMPLE_DIR / "student_sample.csv"
            if sample_path.exists():
                return sample_path
        
        upload_path = UPLOAD_DIR / file_id
        if upload_path.exists():
            return upload_path

        raise AppException(f"Không tìm thấy tập dữ liệu với mã: {file_id}", status_code=404)

    @staticmethod
    def load_dataframe(file_id: str) -> pd.DataFrame:
        """Đọc file CSV thành pandas DataFrame."""
        path = DataService.get_file_path(file_id)
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            raise AppException(f"Lỗi khi đọc file CSV: {str(e)}", status_code=400)

    @staticmethod
    def preview_dataset(file_id: str) -> dict:
        """Lấy thông tin tổng quan và mẫu dữ liệu."""
        df = DataService.load_dataframe(file_id)
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        missing_dict = df.isnull().sum().to_dict()

        return {
            "filename": file_id,
            "total_rows": int(len(df)),
            "total_columns": int(len(df.columns)),
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "missing_values": {k: int(v) for k, v in missing_dict.items()},
            "sample_data": df.head(10).fillna("").to_dict(orient="records")
        }
