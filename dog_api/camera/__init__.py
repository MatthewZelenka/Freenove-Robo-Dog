from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import cv2
from picamera2 import Picamera2

from ..connection_manager import ConnectionManager

router = APIRouter()

camera_manager = ConnectionManager()

"""
Camera api
"""
 
FPS = 30
 
async def read_camera(picam2:Picamera2):
    """
    Function to reading data from an camera
    """
    await asyncio.sleep(1 / FPS)  # Delay between readings
    
    # Capture an image
    frame = picam2.capture_array()
 
    # Convert the image to BGR format if needed
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
 
    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame_bgr)
    frame_bytes = buffer.tobytes()
            
    # Yield the frame bytes
    yield frame_bytes
 
@router.websocket("/camera")
async def camera_websocket_endpoint(websocket: WebSocket):
    await camera_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await camera_manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        camera_manager.disconnect(websocket)
 
async def broadcast_camera_data():
    """
    Background task to broadcast sensor data to all connected clients
    """
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)
    camera_status: bool = False
 
    while True:
        if camera_manager.has_active_connections():
            if not camera_status:
                picam2.start()
                camera_status = True
            else:
                async for frame in read_camera(picam2):
                    if camera_manager.has_active_connections():
                        await camera_manager.broadcast_bytes(frame)
                    else:
                        break
        else:
            if camera_status:
                picam2.stop()
                camera_status = False
            await asyncio.sleep(1)  # Check for active connections periodically
