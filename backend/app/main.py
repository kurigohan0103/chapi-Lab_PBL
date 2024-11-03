# Depends, HTTPException: FastAPIの依存性注入機能およびHTTPエラーハンドリング機能
from fastapi import FastAPI, Depends, HTTPException
# BaseModel: リクエストのデータ構造を定義するために使用
from fastapi.middleware.cors import CORSMiddleware
# engine: SQLAlchemyでデータベース接続を管理するためのオブジェクト
# Base: SQLAlchemyのdeclarative_base()から生成されたベースクラスで，モデルクラスがこのクラスを継承してテーブル定義
from app.database.database import engine, Base
# 認証ルーターをインポート
from .routers import auth


app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    # CORSリクエストを許可するオリジン（ドメイン）を指定
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    # 許可するHTTPメソッドを指定
    allow_methods=["*"],
    # 許可するHTTPヘッダーを指定
    allow_headers=["*"],
)

# テーブルを作成
# bind=engine：どのデータベース接続を使用するかを指定
# アプリケーションの初回実行時やスキーマが必要なときに一度呼び出される．テーブルが存在しない場合にのみ作成される．
Base.metadata.create_all(bind=engine)

# ルーターをアプリに組み込む
# prefixパラメータ：ルーターに属する全てのエンドポイントに共通のパスを指定する
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Security Robot API"}