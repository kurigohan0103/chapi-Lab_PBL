# SQLAlchemyを使用してSQLiteデータベースへの接続を設定し,データベースセッションを管理

# create_engine: データベース接続を作成するための関数．指定されたデータベースURLを基に，Pythonコードとデータベース間の接続を確立する．
from sqlalchemy import create_engine
# sessionmaker: データベースセッションを作成するためのファクトリ関数．セッションはデータベースへのCRUD操作を行う際に必要．
# declarative_base: SQLAlchemy ORMを使用する際に，データベーステーブルのマッピングのベースとなるクラスを生成する．このクラスを継承してテーブルモデルを作成する．
# データベーステーブルとPythonクラスをつなぐための"土台"になるものである．この土台を使ってクラスを作ると，そのクラスがデータベースのテーブルとして動作するようになる．
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLiteデータベースのURL
# ルートディレクトリに security_robot.dbファイルが作成される．
# sqlite:///: SQLiteを使用していることを示している．
DATABASE_URL = "sqlite:///./security_robot.db"

# データベースのエンジン作成
engine = create_engine(
    DATABASE_URL,
    # SQLite特有の条件
    # 同一スレッド制約を無効化し，マルチスレッド環境で接続を許可する．
    connect_args={"check_same_thread": False}
)

# セッションを作成するクラス
# autocommit=False: セッションが自動的にコミットされない．commit() メソッドを呼び出してコミットする必要あり．
# autoflush=False: commit() を呼び出すまでflush()は行われない．
# bind=engine: この SessionLocalクラスは指定されたengineに接続するセッションを作成する．
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemyのベースクラスを作成
Base = declarative_base()

def get_db():
    # SessionLocal() を呼び出してデータベースセッションを作成する．
    db = SessionLocal()
    try:
        # 呼び出し元にセッションを返す．-->セッションを自動的に生成・管理
        yield db
    finally:
        db.close()