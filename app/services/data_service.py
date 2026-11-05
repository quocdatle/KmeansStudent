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
        """Đọc file CSV thành pandas DataFrame, tự động nhận diện dấu phân cách và chuẩn hóa kiểu số."""
        path = DataService.get_file_path(file_id)
        try:
            # Tự động nhận diện dấu phân cách (hỗ trợ cả dấu ',', ';', '\t')
            try:
                df = pd.read_csv(path, sep=None, engine="python")
            except Exception:
                # Nếu sep=None lỗi, thử lần lượt các dấu phân cách phổ biến
                try:
                    df = pd.read_csv(path, sep=";")
                except Exception:
                    df = pd.read_csv(path, sep=",")

            # Làm sạch khoảng trắng tên cột
            df.columns = [str(c).strip().strip('"').strip("'") for c in df.columns]

            # Tự động chuyển đổi các cột số nhưng bị lưu dưới dạng chuỗi (ví dụ: "0", "11") sang numeric
            for col in df.columns:
                if df[col].dtype == object:
                    converted = pd.to_numeric(df[col].astype(str).str.strip().str.strip('"'), errors="coerce")
                    # Nếu hơn 80% giá trị hợp lệ sau khi convert sang số thì coi đó là cột số
                    if converted.notnull().sum() > 0 and (converted.notnull().sum() / len(df)) >= 0.8:
                        df[col] = converted

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
