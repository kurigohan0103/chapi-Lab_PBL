from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.database import SessionLocal
from backend.app.models.models import SecurityMode
from backend.app.schemas.schemas import SecurityMode as SecurityModeSchema, SecurityModeCreate
from datetime import datetime

router = APIRouter()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/security_mode", response_model=SecurityModeSchema)
def get_security_mode(db: Session = Depends(get_db)):
    """警備モードを取得"""
    mode = db.query(SecurityMode).first()
    if not mode:
        raise HTTPException(status_code=404, detail="Security mode not found")
    return mode

@router.put("/security_mode", response_model=SecurityModeSchema)
def update_security_mode(security_mode: SecurityModeCreate, db: Session = Depends(get_db)):
    """警備モードを更新"""
    mode = db.query(SecurityMode).first()
    if not mode:
        mode = SecurityMode(mode=security_mode.mode)
        db.add(mode)
    else:
        mode.mode = security_mode.mode
    db.commit()
    db.refresh(mode)
    # return mode
    # 明示的に辞書型に変換
    return {
        "id": mode.id,
        "mode": mode.mode,
    }
