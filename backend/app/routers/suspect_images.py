from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from backend.app.models.models import SuspectImage
from backend.app.database.database import SessionLocal

router = APIRouter()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ディレクトリ設定
IMAGE_SAVE_DIR = Path("./static/images")

@router.get("/api/suspect_images")
def get_suspect_images(db: Session = Depends(get_db)):
    """
    保存された不審者画像を取得 (新しい順)
    """
    images = db.query(SuspectImage).order_by(SuspectImage.id.desc()).all()

    if not images:
        raise HTTPException(status_code=404, detail="No suspect images found.")

    response = [
        {
            "id": image.id,
            "suspect_id": image.suspect_id,
            "image_url": f"/api/images/suspect/{image.id}"
        }
        for image in images
    ]
    return JSONResponse(content={"images": response})

@router.get("/api/images/suspect/{image_id}")
def get_suspect_image(image_id: int, db: Session = Depends(get_db)):
    """
    指定された ID の画像を返すエンドポイント
    """
    # データベースから画像のパスを取得
    suspect_image = db.query(SuspectImage).filter(SuspectImage.id == image_id).first()

    if not suspect_image:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = Path(suspect_image.image_path).resolve()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
