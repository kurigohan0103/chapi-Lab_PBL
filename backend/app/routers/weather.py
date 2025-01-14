from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.database import SessionLocal
from backend.app.models.models import Weather
from backend.app.schemas.schemas import Weather as WeatherSchema
from typing import List

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/weather/{location}", response_model=WeatherSchema)
def get_weather(location: str, db: Session = Depends(get_db)):
    """
    データベースから特定の location の天気情報を取得
    """
    # データベースで場所に一致する天気情報を検索
    weather_entry = db.query(Weather).filter(Weather.location == location).first()

    if not weather_entry:
        # データベースに存在しない場合、新規追加（ここでは降水確率を仮に 0 に設定）
        weather_entry = Weather(location=location, precipitation_chance=0)
        db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)

    return weather_entry

@router.get("/weather", response_model=List[WeatherSchema])
def get_all_weather(db: Session = Depends(get_db)):
    """
    すべての天気情報を取得
    """
    return db.query(Weather).all()
