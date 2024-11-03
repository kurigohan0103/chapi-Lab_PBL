from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..database import Base  # 相対インポートに変更

# users テーブルの定義
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# robots テーブルの定義
class Robot(Base):
    __tablename__ = 'robots'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# user_robot_access テーブルの定義
class UserRobotAccess(Base):
    __tablename__ = 'user_robot_access'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    robot_id = Column(Integer, ForeignKey('robots.id'), nullable=False)
    role = Column(String)

# security_modes テーブルの定義
class SecurityMode(Base):
    __tablename__ = 'security_modes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    robot_id = Column(Integer, ForeignKey('robots.id'), nullable=False)
    mode = Column(Boolean, default=False)
    updated_at = Column(DateTime)

# weather テーブルの定義
class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    robot_id = Column(Integer, ForeignKey('robots.id'), nullable=False)
    location = Column(String)
    precipitation_chance = Column(Integer)
    updated_at = Column(DateTime)

# suspects テーブルの定義
class Suspect(Base):
    __tablename__ = 'suspects'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    robot_id = Column(Integer, ForeignKey('robots.id'), nullable=False)
    description = Column(String)
    detected_at = Column(DateTime)

# suspect_images テーブルの定義
class SuspectImage(Base):
    __tablename__ = 'suspect_images'
    id = Column(Integer, primary_key=True, index=True)
    suspect_id = Column(Integer, ForeignKey('suspects.id'), nullable=False)
    image_path = Column(String)
    captured_at = Column(DateTime)
