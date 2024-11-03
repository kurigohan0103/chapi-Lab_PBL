from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# .envファイルを読み込んで環境変数を設定
load_dotenv()

# 環境変数からSECRET_KEYを取得。見つからない場合はNoneが返る
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"  # JWTの暗号化アルゴリズムを設定
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # トークンの有効期限を分単位で指定

def create_access_token(data: dict):
    """
    JWTアクセストークンを生成する関数。
    :param data: トークンに含めるペイロードデータ（ユーザー情報など）
    :return: 生成されたJWT
    """
    to_encode = data.copy()  # 元のデータを保護するためにコピーを作成
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # 現在時刻に有効期限を加算して設定
    to_encode.update({"exp": expire})  # ペイロードに有効期限を追加
    
    # JWTを生成し、SECRET_KEYとアルゴリズムで署名
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # 生成されたトークンを返す
