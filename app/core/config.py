from pathlib import Path

# Thư mục gốc dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Đường dẫn thư mục dữ liệu
DATA_DIR = BASE_DIR / "data"
SAMPLE_DIR = DATA_DIR / "sample"
UPLOAD_DIR = DATA_DIR / "uploads"

# Đảm bảo các thư mục luôn tồn tại
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# Cấu hình ứng dụng
APP_TITLE = "K-Means Student Clustering API"
APP_DESCRIPTION = "API phân tích và phân cụm sinh viên sử dụng thuật toán K-Means"
APP_VERSION = "1.0.0"

# Cấu hình file upload
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".csv"]
