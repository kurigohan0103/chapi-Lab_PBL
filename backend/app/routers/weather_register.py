from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Weather
from ..schemas import WeatherCreate
from ..services.auth_service import get_current_user

router = APIRouter()

@router.post("/weather/weather-register")
def register_weather(location: WeatherCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """
    地域情報を登録するエンドポイント．
    ログイン中のユーザーIDとともに地域情報をweatherテーブルに保存する.
    """
    # 新しい地域情報を作成
    new_weather = Weather(user_id=current_user.id, location=location.location)
    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)
    return {"message": "地域情報が登録されました", "data": new_weather}
