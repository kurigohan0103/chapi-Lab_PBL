import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Weather
from ..services.auth_service import get_current_user

router = APIRouter()

# OpenWeatherMap APIの設定
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "your_openweather_api_key"  # OpenWeatherMapのAPIキー

@router.get("/weather/check-rain")
def check_rain(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """
    ログイン中のユーザーの設定地域に基づき、降水確率を取得して返すエンドポイント。
    """
    # ユーザーの地域情報をデータベースから取得
    weather_info = db.query(Weather).filter(Weather.user_id == current_user.id).first()
    if not weather_info:
        raise HTTPException(status_code=404, detail="地域情報が設定されていません")

    # 天気APIから地域の降水確率を取得
    params = {
        "q": weather_info.location,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="天気情報の取得に失敗しました")

    weather_data = response.json()
    precipitation_chance = weather_data.get("rain", {}).get("1h", 0)  # 1時間の降水確率を取得

    return {
        "location": weather_info.location,
        "precipitation_chance": precipitation_chance
    }
