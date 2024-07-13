import io

from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
import asyncio

from connection_manager import ConnectionManager
import ultrasonic

"""
Setting up variables
"""

manager = ConnectionManager()

"""
Set up fastapi server
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    asyncio.create_task(ultrasonic.broadcast_sensor_data())
    yield
    # On death
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(ultrasonic.router)

"""
Functions
"""

"""
Camera stream

# initialize the PiCamera
camera = PiCamera()

# camera settings
camera.resolution = (400, 300)
camera.framerate = 24

# create a circular buffer to store latest frame
stream = io.BytesIO()

# Function to continuously capture frames from camera

def capture_frames():
    global stream
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        # Rewind the stream ready for reading
        stream.seek(0)
        yield stream.read()
        # Reset stream for next frame
        stream.seek(0)
        stream.truncate()

@app.get("/camera")
async def video_feed():
    return Response(content=capture_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
"""
# Optional endpoint to check if the server is running
@app.get("/")
async def read_root():
    return {"message": "FastAPI WebSocket server is running"}

