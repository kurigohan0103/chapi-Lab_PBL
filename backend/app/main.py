from fastapi import FastAPI
from backend.app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.security import router as security_router
from backend.app.routers.weather import router as weather_router
from backend.app.routers.suspect_images import router as suspect_images_router
from backend.app.routers.camera_stream_with_detection import router as detection_router
from fastapi.staticfiles import StaticFiles
import os

# テーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPI アプリケーションの初期化
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーターの登録
app.include_router(security_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(detection_router, prefix="/api")
app.include_router(suspect_images_router, prefix="/api")

# 静的ファイルの設定
static_path = os.path.join(os.path.dirname(__file__), "static")

# app.mount を設定
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    raise RuntimeError(f"Directory '{static_path}' does not exist")