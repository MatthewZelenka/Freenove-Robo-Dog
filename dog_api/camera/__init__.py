
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import cv2

from ..connection_manager import ConnectionManager

router = APIRouter()

camera_manager = ConnectionManager()

"""
Camera api
"""

FPS = 30

async def read_camera(cap:cv2.VideoCapture):
    """
    Function to reading data from an camera
    """
    while True:
        await asyncio.sleep(1/FPS)  # Delay between readings
        
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield frame

@router.websocket("/ws")
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
    cap: cv2.VideoCapture 

    camera_status: bool = False

    while True:
        if camera_manager.has_active_connections():
            if not camera_status:
                cap = cv2.VideoCapture(0)
                camera_status = True
            else:
                async for frame in read_camera(cap):
                    if camera_manager.has_active_connections():
                        await camera_manager.broadcast_bytes(frame)
                    else:
                        break
        else:
            
            if camera_status:
                cap.release()
                camera_status = False
            await asyncio.sleep(1)  # Check for active connections periodically
