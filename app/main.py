from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, BASE_DIR
from app.core.exceptions import AppException, app_exception_handler
from app.api.routes import api_router

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký custom exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Đăng ký API router
app.include_router(api_router)

# Mount thư mục Frontend tĩnh
frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
