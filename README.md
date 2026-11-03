# 🎓 Hệ Thống Phân Cụm Sinh Viên (K-Means Clustering)

Dự án ứng dụng thuật toán học máy không giám sát **K-Means Clustering** để phân tích, phân nhóm hồ sơ học tập của sinh viên dựa trên hành vi và kết quả học tập.

Hệ thống được xây dựng theo đúng yêu cầu nghiệp vụ và tuân thủ toàn bộ quy chuẩn tại [STANDARDS.md](STANDARDS.md).

---

## 🚀 Công Nghệ Sử Dụng (Tech Stack)

- **Xử lý dữ liệu & Thuật toán:** `Python`, `pandas`, `scikit-learn`, `numpy`
- **Backend API:** `FastAPI`, `Uvicorn`, `Pydantic`
- **Frontend:** `HTML5`, `CSS3 (Tailwind CSS)`, `Vanilla JS`, `Chart.js`
- **Lưu trữ dữ liệu:** `CSV Files`

---

## 📌 Các Tính Năng Chính

1. **Quản lý tập dữ liệu:**
   - Chọn bộ dữ liệu mẫu sinh viên chuẩn bị sẵn (`student_sample.csv`).
   - Tải lên (upload) file CSV tùy chỉnh từ máy tính.
   - Xem trước bảng dữ liệu (Preview) và thống kê đặc trưng số.
2. **Tiền xử lý & Chuẩn hóa (Feature Scaling):**
   - Lựa chọn linh hoạt các đặc trưng số để đưa vào mô hình.
   - Chuẩn hóa bắt buộc với K-Means: `StandardScaler` (mặc định) hoặc `MinMaxScaler`.
3. **Xác định số cụm K tối ưu:**
   - Biểu đồ **Elbow Method** (Inertia / SSE).
   - Biểu đồ **Silhouette Score** và tự động đề xuất số cụm K tốt nhất.
4. **Huấn luyện K-Means & Trực quan hóa 2D (PCA):**
   - Huấn luyện mô hình K-Means theo K đã chọn.
   - Giảm chiều dữ liệu bằng PCA xuống 2D để hiển thị Scatter Plot các cụm kèm theo vị trí tâm cụm (Centroids).
5. **Hồ sơ phân cụm (Cluster Profiles):**
   - Thống kê giá trị trung bình từng đặc trưng cho mỗi nhóm sinh viên.
   - Phân tích tỷ lệ phân bổ phần trăm giữa các cụm.
6. **Dự đoán & Giải thích sinh viên mới:**
   - Form nhập hồ sơ của 1 sinh viên mới.
   - Dự đoán sinh viên thuộc cụm nào dựa trên khoảng cách Euclidean đến các tâm cụm.
   - Giải thích chi tiết nguyên nhân xếp vào cụm dựa trên độ tương đồng của các chỉ số.

---

## 📂 Cấu Trúc Thư Mục Dự Án

Chi tiết cấu trúc mô-đun được tổ chức theo kiến trúc phân tầng:

```text
Kmeans/
├── app/
│   ├── main.py                     # Entry point khởi chạy FastAPI & StaticFiles
│   ├── api/
│   │   ├── routes.py               # Router tổng hợp
│   │   └── endpoints/              # Tách biệt API theo chức năng
│   │       ├── dataset.py          # Upload CSV & Preview
│   │       ├── analysis.py         # Phân tích Elbow & Silhouette
│   │       ├── clustering.py       # Huấn luyện K-Means & PCA
│   │       └── predict.py          # Dự đoán & giải thích cụm
│   ├── core/
│   │   ├── config.py               # Thiết lập cấu hình hệ thống
│   │   └── exceptions.py           # Bộ bắt và xử lý ngoại lệ chuẩn hóa
│   ├── schemas/                    # Pydantic Schemas định nghĩa Request/Response
│   └── services/                   # Logic nghiệp vụ & Machine Learning Core
├── data/
│   ├── sample/
│   │   └── student_sample.csv      # Dataset mẫu sinh viên
│   └── uploads/                    # Thư mục chứa file tải lên
├── frontend/                       # Giao diện người dùng
│   ├── index.html                  # Giao diện chính
│   ├── css/style.css               # Tùy biến giao diện
│   └── js/
│       ├── api.js                  # Gọi REST API
│       ├── charts.js               # Biểu đồ Chart.js
│       └── app.js                  # Điều phối sự kiện giao diện
├── tests/                          # Thư mục kiểm thử
├── requirements.txt                # Thư viện phụ thuộc
├── STANDARDS.md                    # Quy chuẩn chi tiết dự án
└── README.md
```

---

## ⚙️ Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Clone repository & mở thư mục dự án

```bash
git clone https://github.com/quocdatle/KmeansStudent.git
cd KmeansStudent
```

### 2. Cài đặt môi trường ảo Python

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# (Lưu ý: Nếu gặp lỗi ExecutionPolicy trên PowerShell, chạy trước: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

# Windows (Command Prompt):
venv\Scripts\activate.bat

# macOS / Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng

```bash
# Cách 1: Khởi chạy khi đã kích hoạt môi trường ảo
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Cách 2: Khởi chạy trực tiếp bằng python trong venv (không cần kích hoạt môi trường)
# Windows:
.\venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Linux / macOS:
./venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Trải nghiệm hệ thống

- **Giao diện Web:** Truy cập trình duyệt tại [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Tài liệu Swagger API Docs:** Truy cập [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📖 Quy Chuẩn Dự Án

Vui lòng đọc kỹ tài liệu [STANDARDS.md](STANDARDS.md) trước khi tham gia phát triển mã nguồn để nắm rõ:

- Chuẩn kiến trúc và phân tầng Clean/Modular FastAPI.
- Chuẩn toán học & ML (chuẩn hóa dữ liệu, PCA, Silhouette, Distance to centroids).
- Chuẩn mã nguồn Python PEP 8 & JavaScript ES6+.
- Chuẩn commit Git theo Conventional Commits.
