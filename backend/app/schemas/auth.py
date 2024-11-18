from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# 認証トークンのレスポンスモデル
# APIでログイン後に返されるトークン情報を表す．
class Token(BaseModel):
    # 認証に使用されるアクセストークン
    access_token: str
    # トークンのタイプ（通常は "Bearer"）
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None  # トークン内に含まれるユーザー名を保持
