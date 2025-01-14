from pydantic import BaseModel
from datetime import datetime

class SecurityModeBase(BaseModel):
    mode: bool

class SecurityModeCreate(SecurityModeBase):
    pass

class SecurityMode(SecurityModeBase):
    id: int
    class Config:
        orm_mode = True

class WeatherBase(BaseModel):
    location: str
    precipitation_chance: float

class WeatherCreate(WeatherBase):
    pass

class Weather(WeatherBase):
    id: int

    class Config:
        orm_mode = True

class SuspectImageBase(BaseModel):
    suspect_id: int
    image_data: str  # Base64 エンコードされた画像データ
    captured_at: datetime

class SuspectImageCreate(SuspectImageBase):
    pass

class SuspectImage(SuspectImageBase):
    id: int
    captured_at: datetime

    class Config:
        orm_mode = True
