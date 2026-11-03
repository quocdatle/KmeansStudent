import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.core.config import UPLOAD_DIR, ALLOWED_EXTENSIONS
from app.core.exceptions import AppException
from app.services.data_service import DataService

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.get("/preview/{file_id}")
async def get_dataset_preview(file_id: str):
    data = DataService.preview_dataset(file_id)
    return {"success": True, "data": data}

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise AppException("Chỉ chấp nhận tệp định dạng .csv", status_code=400)

    save_path = UPLOAD_DIR / file.filename
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise AppException(f"Không thể lưu tệp: {str(e)}", status_code=500)

    preview = DataService.preview_dataset(file.filename)
    return {
        "success": True,
        "message": "Tải lên dataset thành công",
        "file_id": file.filename,
        "data": preview
    }
