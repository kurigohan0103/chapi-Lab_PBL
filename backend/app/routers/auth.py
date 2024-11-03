from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db  # データベースセッションを取得する関数をインポート
from ..services.auth_service import create_user, authenticate_user, invalidate_token  # ユーザー作成、認証、トークン無効化関数をインポート
from ..services.token_service import create_access_token  # JWTを生成する関数をインポート
from ..schemas.auth import UserCreate, UserLogin, Token  # リクエストやレスポンスで使用するスキーマをインポート

# 認証用のAPIルーターを作成
router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    新しいユーザーを登録するエンドポイント。
    ユーザーが正常に登録された後、JWTトークンを返す。
    :param user: ユーザー作成用のデータ
    :param db: データベースセッション
    :return: アクセストークン
    """
    db_user = create_user(db, user)  # 新しいユーザーを作成
    access_token = create_access_token(data={"sub": db_user.username})  # トークンを生成
    return {"access_token": access_token, "token_type": "bearer"}  # トークンを返す

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    ユーザーのログインを処理するエンドポイント。
    ユーザーが認証されると、JWTトークンを返す。
    :param user: ログイン用のユーザーデータ
    :param db: データベースセッション
    :return: アクセストークン
    """
    db_user = authenticate_user(db, user.username, user.password)  # ユーザー認証
    if not db_user:  # 認証に失敗した場合
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # ステータスコード401を返す
            detail="Invalid username or password",  # エラーメッセージを指定
            headers={"WWW-Authenticate": "Bearer"},  # 認証スキームを指定
        )
    access_token = create_access_token(data={"sub": db_user.username})  # トークンを生成
    return {"access_token": access_token, "token_type": "bearer"}  # トークンを返す

@router.post("/logout")
def logout(token: str = Depends(invalidate_token)):
    """
    ログアウト処理を行うエンドポイント。
    トークンを無効化することで、セッションを終了。
    :param token: ログアウト時に無効化するトークン
    :return: ログアウト成功メッセージ
    """
    return {"message": "Logged out successfully"}  # ログアウト成功メッセージを返す
