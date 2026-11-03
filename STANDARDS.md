# QUY CHUẨN DỰ ÁN K-MEANS CLUSTERING SYSTEM

Tài liệu này định nghĩa toàn bộ quy chuẩn kỹ thuật, kiến trúc hệ thống, quy ước viết mã (coding conventions), quy trình xử lý dữ liệu và luồng phát triển cho dự án **Phân cụm sinh viên sử dụng thuật toán K-Means**.

---

## 1. TỔNG QUAN DỰ ÁN & TECH STACK

Dự án phát triển một ứng dụng phân tích và phân cụm dữ liệu sinh viên dựa trên hành vi học tập và kết quả học tập, ứng dụng mô hình học máy không giám sát **K-Means Clustering**.

| Tầng (Layer) | Công nghệ chính | Vai trò & Mục đích |
|---|---|---|
| **Xử lý dữ liệu & Thuật toán** | `Python 3.10+`, `pandas`, `scikit-learn`, `numpy` | Đọc dữ liệu, tiền xử lý, chuẩn hóa, huấn luyện K-Means, tính toán Elbow/Silhouette, giảm chiều PCA |
| **Backend API** | `FastAPI`, `Uvicorn`, `Pydantic` | Cung cấp RESTful API hiệu năng cao, xác thực dữ liệu đầu vào/ra, điều phối các services |
| **Frontend** | `HTML5`, `CSS3`, `Vanilla JavaScript`, `Chart.js` | Giao diện tương tác người dùng, trực quan hóa biểu đồ phân cụm (Elbow, Silhouette, Scatter PCA 2D, Cluster Profile) |
| **Lưu trữ** | `CSV Files` | Lưu trữ dataset mẫu và các file dữ liệu người dùng tải lên |

---

## 2. KIẾN TRÚC THƯ MỤC DỰ ÁN

Hệ thống được thiết kế theo kiến trúc phân tầng (Layered Architecture) tách bạch rõ ràng giữa Presentation, API, Business Logic và Data Access.

```text
Kmeans/
├── app/                              # Mã nguồn chính Backend (FastAPI)
│   ├── __init__.py
│   ├── main.py                       # Điểm khởi chạy FastAPI, cấu hình CORS, mount static
│   ├── api/                          # Tầng định tuyến (Routing & Controllers)
│   │   ├── __init__.py
│   │   ├── routes.py                 # Gom các router endpoint
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── dataset.py            # API Upload CSV, chọn dataset mẫu, preview
│   │       ├── preprocess.py         # API cấu hình tiền xử lý & chuẩn hóa
│   │       ├── analysis.py           # API tính Elbow method & Silhouette scores
│   │       ├── clustering.py         # API huấn luyện K-Means, PCA 2D, Cluster Profile
│   │       └── predict.py            # API dự đoán cụm & giải thích cho sinh viên mới
│   ├── core/                         # Cấu hình lõi & tiện ích dùng chung
│   │   ├── __init__.py
│   │   ├── config.py                 # Đọc cấu hình, biến môi trường, đường dẫn lưu file
│   │   └── exceptions.py             # Custom Exception Handlers chuẩn hóa phản hồi lỗi
│   ├── schemas/                      # Pydantic Schemas (Request/Response Models)
│   │   ├── __init__.py
│   │   ├── dataset.py                # Schema metadata dataset, preview dữ liệu
│   │   ├── clustering.py             # Schema tham số K, kết quả Elbow, Silhouette, PCA, Profile
│   │   └── predict.py                # Schema dữ liệu đầu vào sinh viên mới & kết quả dự đoán
│   └── services/                     # Tầng Business Logic & Machine Learning Core
│       ├── __init__.py
│       ├── data_service.py           # Đọc/ghi CSV, thống kê mô tả, kiểm tra dữ liệu
│       ├── kmeans_service.py         # Tiền xử lý, chuẩn hóa, K-Means, PCA, Elbow, Silhouette
│       └── prediction_service.py     # Suy luận cụm cho mẫu mới và logic sinh lời giải thích
├── data/                             # Lưu trữ dữ liệu
│   ├── sample/                       # Dataset mẫu đi kèm dự án
│   │   └── student_sample.csv        # Dữ liệu mẫu hồ sơ học tập sinh viên
│   └── uploads/                      # Thư mục chứa các file CSV người dùng upload
│       └── .gitkeep
├── frontend/                         # Giao diện người dùng Web tĩnh
│   ├── index.html                    # Single Page Application UI
│   ├── css/
│   │   └── style.css                 # Giao diện tùy biến, responsive
│   └── js/
│       ├── api.js                    # Module gọi REST API đến Backend
│       ├── charts.js                 # Module cấu hình và vẽ đồ thị bằng Chart.js
│       └── app.js                    # Controller điều phối tương tác UI
├── tests/                            # Kiểm thử tự động (Unit & Integration Tests)
│   ├── __init__.py
│   └── test_kmeans.py
├── .gitignore                        # Cấu hình bỏ qua tệp tin rác trong Git
├── requirements.txt                  # Danh sách dependencies thư viện Python
├── README.md                         # Hướng dẫn tổng quan & khởi chạy nhanh
└── STANDARDS.md                      # Tài liệu quy chuẩn dự án (file này)
```

---

## 3. QUY CHUẨN THUẬT TOÁN & XỬ LÝ DỮ LIỆU (ML STANDARDS)

### 3.1. Tiền xử lý dữ liệu (Data Preprocessing)
1. **Xử lý giá trị bị thiếu (Missing Values):**
   - Phải cung cấp tùy chọn rõ ràng cho người dùng:
     - `drop`: Loại bỏ các dòng chứa `NaN`.
     - `impute_mean`: Điền giá trị trung bình (đối với đặc trưng liên tục phân phối chuẩn).
     - `impute_median`: Điền giá trị trung vị (đối với đặc trưng có độ lệch hoặc có outliers).
2. **Loại bỏ cột định danh / không phải số:**
   - Các cột mã định danh (như `student_id`, `name`) hoặc nhãn phi số phải được tách ra làm metadata trước khi đưa vào tính toán ma trận số học.

### 3.2. Chuẩn hóa đặc trưng (Feature Scaling - Bắt buộc)
- **Lý do khoa học:** K-Means sử dụng khoảng cách Euclidean (\(d(p, q) = \sqrt{\sum (p_i - q_i)^2}\)) để phân cụm. Các đặc trưng có thang đo lớn (ví dụ: `study_hours` từ 0-40 so với `attendance_rate` từ 0-100) sẽ chi phối hoàn toàn khoảng cách nếu không được đưa về cùng thang đo.
- **Phương pháp hỗ trợ:**
  - `StandardScaler`: Đưa về mean = 0, std = 1 (\(z = \frac{x - \mu}{\sigma}\)) - Khuyến nghị mặc định.
  - `MinMaxScaler`: Đưa về khoảng [0, 1] (\(x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}\)).
- **Lưu ý triển khai:** Đối tượng scaler (fit trên tập huấn luyện) phải được lưu giữ hoặc tái sử dụng khi dự đoán dữ liệu mới của sinh viên.

### 3.3. Xác định số cụm tối ưu K (Optimal K Selection)
1. **Phương pháp Elbow (Inertia):**
   - Chạy K-Means với \(K \in [2, 10]\).
   - Ghi nhận `inertia_` (tổng bình phương khoảng cách từ mỗi điểm đến tâm cụm gần nhất).
   - Vẽ đường cong Elbow để người dùng quan sát điểm "khuỷu tay".
2. **Silhouette Score:**
   - Tính hệ số `silhouette_score(X, labels)` cho mỗi \(K\).
   - Hệ số nhận giá trị từ -1 đến 1. Điểm cao thể hiện các cụm cô đặc và tách biệt rõ rệt.
   - Hệ thống gợi ý tự động giá trị \(K\) có Silhouette Score cao nhất.

### 3.4. Giảm chiều dữ liệu bằng PCA (Principal Component Analysis)
- Dữ liệu học tập thường đa chiều (> 3 đặc trưng), không thể vẽ trực tiếp trên đồ thị 2D.
- Sử dụng `PCA(n_components=2)` trên dữ liệu đã chuẩn hóa để chiếu xuống 2 thành phần chính (PC1, PC2).
- Trả về tọa độ 2D của từng mẫu dữ liệu kèm theo nhãn cụm để Chart.js hiển thị Scatter Plot.
- Cung cấp tỷ lệ phương sai giải thích (`explained_variance_ratio_`) của 2 thành phần chính để đánh giá độ tin cậy của biểu đồ.

### 3.5. Hồ sơ từng cụm (Cluster Profiling)
- Tính toán giá trị trung bình (`mean`) và độ lệch chuẩn (`std`) của từng đặc trưng gốc (chưa chuẩn hóa) theo từng cụm.
- Sinh nhãn ngữ nghĩa mô tả tự động (Semantic Auto-labeling), ví dụ:
  - Cụm có điểm số cao, nghỉ học thấp \(\rightarrow\) *"Chăm chỉ, thành tích cao"*.
  - Cụm có thời gian học thấp, vắng nhiều, điểm thấp \(\rightarrow\) *"Nguy cơ học vụ, cần hỗ trợ"*.
  - Cụm có điểm trung bình, tham gia đều \(\rightarrow\) *"Học lực khá, ổn định"*.

### 3.6. Dự đoán & Giải thích sinh viên mới (Inference & Explanation)
- Đầu vào: Vector đặc trưng của sinh viên mới.
- Xử lý: Áp dụng scaler đã fit \(\rightarrow\) Tính khoảng cách Euclidean đến tất cả tâm cụm \(\rightarrow\) Gán vào cụm có khoảng cách nhỏ nhất.
- Giải thích (Explainability):
  - So sánh giá trị từng môn/thời gian học của sinh viên với giá trị trung bình của cụm đó.
  - Chỉ ra lý do vì sao sinh viên thuộc cụm (ví dụ: *"Sinh viên có số buổi vắng học (12 buổi) và số giờ tự học (4h/tuần) gần với đặc trưng trung bình của Cụm 1"*).

---

## 4. QUY CHUẨN BACKEND API (FASTAPI)

### 4.1. Nguyên tắc thiết kế RESTful
- Sử dụng đúng HTTP Methods:
  - `GET`: Lấy dữ liệu, xem preview, danh sách dataset mẫu.
  - `POST`: Tải lên tệp tin, tính toán Elbow/Silhouette, huấn luyện phân cụm, dự đoán.
- Tất cả endpoints phải có prefix `/api/v1`.

### 4.2. Cấu trúc Response chuẩn hóa
Mọi phản hồi từ API phải tuân theo cấu trúc JSON chuẩn:

```json
// Thành công (HTTP 200/201)
{
  "success": true,
  "message": "Huấn luyện K-Means thành công",
  "data": { ... }
}

// Thất bại (HTTP 400/404/422/500)
{
  "success": false,
  "message": "Dữ liệu chứa giá trị không hợp lệ",
  "errors": [ ... ]
}
```

### 4.3. Quản lý trạng thái & File
- Khi upload CSV, lưu file vào `data/uploads/` với tên file an toàn (sử dụng UUID hoặc timestamp để tránh trùng lặp).
- Kiểm tra dung lượng file (giới hạn tối đa 10MB) và định dạng phần mở rộng (chỉ chấp nhận `.csv`).

---

## 5. QUY CHUẨN FRONTEND & CHART.JS

### 5.1. Tổ chức mã nguồn Frontend
- Không lồng ghép logic xử lý dữ liệu nặng ở Frontend; Frontend chỉ đóng vai trò render và gọi API.
- Tách biệt rõ:
  - `api.js`: Chuyên trách `fetch()` với Backend, xử lý try/catch và định dạng response.
  - `charts.js`: Quản lý vòng đời các instance của Chart.js (`destroy()` trước khi vẽ mới để tránh leak bộ nhớ).
  - `app.js`: Lắng nghe sự kiện người dùng (click, submit, change), quản lý trạng thái hiển thị (loading spinner, alerts).

### 5.2. Các biểu đồ trực quan hóa
1. **Biểu đồ Elbow (Line Chart):** Trục X là số cụm K (2 đến 10), trục Y là Inertia.
2. **Biểu đồ Silhouette (Bar Chart / Line Chart):** Trục X là số cụm K, trục Y là Silhouette Score (thể hiện đường ngưỡng tối ưu).
3. **Biểu đồ Scatter PCA 2D:**
   - Mỗi cụm là một dataset riêng biệt có màu sắc phân biệt rõ ràng.
   - Điểm tâm cụm (Centroid) được vẽ to hơn với biểu tượng khác (dấu sao hoặc dấu cộng).
   - Tooltip hiển thị `student_id` và thông tin tóm tắt khi hover chuột.
4. **Biểu đồ Radar / Bar Chart cho Cluster Profiles:** So sánh tương quan các chỉ số trung bình giữa các cụm.

---

## 6. QUY ƯỚC VIẾT MÃ (CODING CONVENTIONS)

### 6.1. Python (PEP 8)
- Sử dụng Type Hints đầy đủ cho tham số và kiểu trả về của hàm:
  ```python
  def fit_kmeans(data: pd.DataFrame, n_clusters: int = 3) -> dict: ...
  ```
- Tên biến/hàm: `snake_case` (ví dụ: `calculate_silhouette_score`).
- Tên class: `PascalCase` (ví dụ: `KMeansService`).
- Tên hằng số: `UPPER_SNAKE_CASE` (ví dụ: `MAX_UPLOAD_SIZE_MB = 10`).
- Docstring chuẩn Google format cho các hàm tính toán phức tạp.

### 6.2. JavaScript (ES6+)
- Sử dụng `const` và `let`, tuyệt đối không dùng `var`.
- Sử dụng `async/await` thay cho Promise chaining phức tạp.
- Đặt tên hàm/biến theo chuẩn `camelCase`.

---

## 7. QUY CHUẨN QUẢN LÝ MÃ NGUỒN (GIT WORKFLOW)

### 7.1. Định dạng Commit Message (Conventional Commits)
Cú pháp: `<type>(<scope>): <subject>`

Các `type` được chấp nhận:
- `feat`: Tính năng mới (ví dụ: `feat(clustering): thêm tính toán PCA 2D scatter plot`)
- `fix`: Sửa lỗi (ví dụ: `fix(preprocess): xử lý ngoại lệ khi thiếu cột số`)
- `docs`: Cập nhật tài liệu (ví dụ: `docs: bổ sung hướng dẫn chạy API`)
- `style`: Định dạng mã, không thay đổi logic (format code, thêm dấu cách)
- `refactor`: Tái cấu trúc mã nguồn nhưng không đổi chức năng
- `test`: Thêm hoặc chỉnh sửa test case
- `chore`: Cập nhật cấu hình build, thêm thư viện

### 7.2. Chiến lược phân nhánh (Branching)
- `main`: Nhánh production ổn định, luôn sẵn sàng chạy.
- `develop`: Nhánh tích hợp các tính năng trước khi release.
- `feature/<tên-tính-năng>`: Nhánh làm việc cho từng chức năng riêng biệt.

---

## 8. DANH MỤC CÁC CHỨC NĂNG CẦN HOÀN THIỆN THEO TECHSTACK

| STT | Chức năng | Trạng thái kiến trúc | Mô tả chi tiết |
|---|---|---|---|
| 1 | **Dataset Management** | `app/api/endpoints/dataset.py` | Upload file CSV người dùng hoặc chọn dataset mẫu (`student_sample.csv`). Trả về preview 5 dòng đầu và thống kê số cột/dòng. |
| 2 | **Data Preprocessing** | `app/api/endpoints/preprocess.py` | Lựa chọn cột đặc trưng huấn luyện, xử lý missing value (`drop`/`impute`), chọn bộ chuẩn hóa (`StandardScaler`/`MinMaxScaler`). |
| 3 | **K Selection Analysis** | `app/api/endpoints/analysis.py` | Tính toán giá trị Inertia (Elbow) và Silhouette score cho \(K = 2 \rightarrow 10\). Gợi ý K tối ưu. |
| 4 | **K-Means & PCA Visualization**| `app/api/endpoints/clustering.py` | Chạy K-Means theo K đã chọn, chiếu PCA xuống 2D, trả về dữ liệu scatter plot cho từng cụm và tọa độ centroids. |
| 5 | **Cluster Profiling** | `app/api/endpoints/clustering.py` | Tính giá trị trung bình từng đặc trưng theo cụm, tự động gán nhãn ngữ nghĩa mô tả nhóm sinh viên. |
| 6 | **Student Inference & Explanation** | `app/api/endpoints/predict.py` | Form nhập thông tin 1 sinh viên mới, dự đoán cụm thuộc về và giải thích chi tiết lý do dựa trên độ lệch đặc trưng so với tâm cụm. |
