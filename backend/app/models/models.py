from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database.database import Base

# 警備モードを管理するテーブル
class SecurityMode(Base):
    __tablename__ = "security_modes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mode = Column(Boolean, default=False, nullable=False)
    

# 天気データを管理するテーブル
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    location = Column(String, nullable=False)
    precipitation_chance = Column(Float, nullable=False)
    
# 不審者情報を管理するテーブル
class Suspect(Base):
    __tablename__ = "suspects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    images = relationship("SuspectImage", back_populates="suspect", cascade="all, delete")

# 不審者画像を管理するテーブル
class SuspectImage(Base):
    __tablename__ = "suspect_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    suspect_id = Column(Integer, ForeignKey("suspects.id"), nullable=False)
    image_path = Column(String, nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    suspect = relationship("Suspect", back_populates="images")

# class SuspectImage(Base):
#     __tablename__ = "suspect_images"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     suspect_id = Column(Integer, ForeignKey("suspects.id"), nullable=False)
#     image_data = Column(LargeBinary, nullable=False)  # 画像データをバイナリ形式で保存
#     captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)

#     suspect = relationship("Suspect", back_populates="images")
