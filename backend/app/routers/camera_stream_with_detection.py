from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from backend.app.database.database import SessionLocal
from backend.app.models.models import SuspectImage, SecurityMode
import cv2
import datetime
import time
import os
from ultralytics import YOLO
from pathlib import Path
import pygame  # 音声再生用ライブラリ
import atexit

router = APIRouter()

# グローバル設定
CONFIDENCE_THRESHOLD = 0.9  # 信頼度閾値
DETECTION_PAUSE_TIME = 30  # 検出間隔 (秒)
LAST_DETECTION_TIME = 0  # 最後に検出した時間
BASE_DIR = Path(__file__).resolve().parent.parent
ALERT_SOUND_PATH = BASE_DIR / "static" / "alert.mp3"  # アラート音声ファイルの絶対パス

# ディレクトリ設定
IMAGE_SAVE_DIR = BASE_DIR / "static" / "images"
IMAGE_SAVE_DIR.mkdir(parents=True, exist_ok=True)  # ディレクトリが存在しない場合に作成

# カメラデバイスの初期化
try:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("カメラデバイスを初期化できませんでした。")
except Exception as e:
    raise RuntimeError(f"カメラデバイスの初期化中にエラーが発生しました: {e}")

# YOLOv8モデルのロード
try:
    model = YOLO("yolov8n.pt")  # 必要に応じてモデルファイルを変更
except Exception as e:
    raise RuntimeError(f"YOLOモデルの読み込み中にエラーが発生しました: {e}")

# データベースセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# セキュリティモードを確認
def is_security_mode_enabled(db: Session) -> bool:
    """セキュリティモードがオンかどうかを確認"""
    mode = db.query(SecurityMode).first()
    return mode.mode if mode else False

# 不審者画像をローカルに保存し、データベースに登録
def save_suspect_image(frame, suspect_id: int, db: Session) -> None:
    """不審者画像を保存"""
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = f"suspect_{suspect_id}_{timestamp}.jpg"
    file_path = IMAGE_SAVE_DIR / file_name

    # フレームを保存
    cv2.imwrite(str(file_path), frame)
    print(f"画像が保存されました: {file_path}")  # 保存先をログに出力

    # データベースに画像情報を登録
    suspect_image = SuspectImage(
        suspect_id=suspect_id,
        image_path=str(file_path),
        captured_at=datetime.datetime.utcnow()
    )
    db.add(suspect_image)
    db.commit()
    db.refresh(suspect_image)

# アラート音を再生
def play_alert_sound():
    """アラート音を再生"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(ALERT_SOUND_PATH))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # 再生が終了するまで待機
            time.sleep(0.1)
        print("アラート音を再生しました。")
    except Exception as e:
        print(f"アラート音の再生中にエラーが発生しました: {e}")

# 映像ストリームの生成
def generate_frames_with_detection(db: Session):
    """セキュリティモードがオンの場合に物体検出を行い、ストリームを生成"""
    global LAST_DETECTION_TIME

    while True:
        # セキュリティモードがオフの場合は待機
        if not is_security_mode_enabled(db):
            print("セキュリティモードがオフのため、検知を停止しています。")
            time.sleep(1)
            continue

        # カメラからフレームを取得
        success, frame = camera.read()
        if not success:
            print("カメラフレームを取得できませんでした。")
            break

        current_time = time.time()

        # 検出をスキップする条件
        if current_time - LAST_DETECTION_TIME < DETECTION_PAUSE_TIME:
            _, buffer = cv2.imencode(".jpg", frame)
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
            continue

        # YOLOで物体検出を実行
        results = model.predict(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])  # クラスIDを取得
                conf = box.conf[0]  # 信頼度を取得

                if cls_id == 0 and conf > CONFIDENCE_THRESHOLD:  # 「人」と判定
                    # 不審者画像を保存
                    save_suspect_image(frame, suspect_id=1, db=db)  # suspect_idは仮置き
                    LAST_DETECTION_TIME = current_time
                    
                    # アラート音を再生
                    play_alert_sound()

        # フレームをエンコードして送信
        _, buffer = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

# ストリームのエンドポイント
@router.get("/video_feed_with_detection")
def video_feed_with_detection(db: Session = Depends(get_db)):
    """物体検出付きのカメラストリームエンドポイント"""
    return StreamingResponse(
        generate_frames_with_detection(db),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# 保存された不審者画像を取得
@router.get("/suspect_images")
def get_suspect_images(db: Session = Depends(get_db)):
    """保存された不審者画像を取得"""
    images = db.query(SuspectImage).order_by(SuspectImage.id.desc()).all()

    if not images:
        raise HTTPException(status_code=404, detail="No suspect images found.")

    response = [
        {
            "id": image.id,
            "suspect_id": image.suspect_id,
            "image_url": f"/static/images/{os.path.basename(image.image_path)}"
        }
        for image in images
    ]
    return JSONResponse(content={"images": response})

# アラート音のテスト再生
@router.get("/test_alert_sound")
def test_alert_sound():
    """アラート音のテスト再生"""
    try:
        play_alert_sound()
        return {"message": "Alert sound played successfully."}
    except Exception as e:
        return {"error": f"Failed to play alert sound: {e}"}

# 静的ファイル提供のテスト
@router.get("/static_test")
def static_test():
    """静的ファイル提供のテスト"""
    test_path = IMAGE_SAVE_DIR / "test.jpg"
    if test_path.exists():
        return {"message": "Static files are accessible."}
    return {"error": "Static file test.jpg not found."}

# アプリケーションのリソース解放
def release_resources():
    """アプリケーション終了時にリソースを解放"""
    global camera
    if camera.isOpened():
        camera.release()
        print("カメラを解放しました。")

atexit.register(release_resources)
