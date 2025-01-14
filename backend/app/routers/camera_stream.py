from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import cv2

router = APIRouter()

# カメラを初期化
camera = cv2.VideoCapture(0)  # デバイスID (0)

def generate_frames():
    """カメラ映像をストリームとして提供"""
    while True:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@router.get("/video_feed")
def video_feed():
    """カメラストリームエンドポイント"""
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
