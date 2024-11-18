# CryptContext: passlibを使ってパスワードのハッシュ化や検証を簡単に行うためのコンテキスト
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User  # ユーザーモデルをインポート
from ..schemas.auth import UserCreate  # ユーザー作成用スキーマ
from app.token_service import SECRET_KEY, ALGORITHM  # token_serviceからインポート


# pwd_context: bcryptを利用してパスワードのハッシュ化と検証を行うための設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    入力されたパスワードをハッシュ化する関数．
    :param password: 平文のパスワード
    :return: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    平文のパスワードとハッシュ化されたパスワードを比較して一致するかを確認する関数．
    :param plain_password: 平文のパスワード
    :param hashed_password: ハッシュ化されたパスワード
    :return: パスワードが一致するかを示すブール値
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    """
    新しいユーザーをデータベースに作成する関数．
    :param db: データベースセッション
    :param user: ユーザー作成用のデータ
    :return: 作成されたユーザーオブジェクト
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    # 入力されたパスワードをハッシュ化
    hashed_password = get_password_hash(user.password)
    # 新しいユーザーオブジェクトを作成
    db_user = User(username=user.username, password_hash=hashed_password)
    db.add(db_user)  # データベースにユーザーを追加
    db.commit()  # 変更をコミットして保存
    db.refresh(db_user)  # 最新のユーザー情報を取得
    return db_user  # 作成されたユーザーを返す

def authenticate_user(db: Session, username: str, password: str):
    """
    ユーザー認証を行う関数．
    :param db: データベースセッション
    :param username: ユーザー名
    :param password: 平文のパスワード
    :return: 認証に成功したユーザーオブジェクトまたはFalse
    """
    # ユーザー名に基づいてユーザーを取得
    user = db.query(User).filter(User.username == username).first()
    # ユーザーが存在しない、またはパスワードが一致しない場合はFalseを返す
    if not user or not verify_password(password, user.password_hash):
        return False
    return user  # 認証に成功したユーザーを返す

def invalidate_token(token: str):
    """
    トークンを無効化する関数．
    この関数ではトークンをブラックリストに追加し，以降のリクエストで無効とする．
    :param token: 無効化するトークン
    """
    # 実際の実装では，Redisやデータベースにトークンを保存するなどの方法を取ることが多い．
    blacklisted_tokens = set()  # 仮のセットで管理
    blacklisted_tokens.add(token)
    return {"message": "Token has been invalidated"}

# トークンから現在のユーザーを取得する関数
def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # トークンのデコードとペイロードの検証
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # データベースからユーザーを取得
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user