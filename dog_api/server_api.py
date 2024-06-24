from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import asyncio
import RPi.GPIO as GPIO

from connection_manager import ConnectionManager
from RPi_ultrasonic import ultrasonic

manager = ConnectionManager()

ultrasonic_sensor = ultrasonic(trigger_pin=27, echo_pin=22, GPIO_Mode=GPIO.BCM)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    asyncio.create_task(broadcast_sensor_data())
    yield
    # On death
    pass

app = FastAPI(lifespan=lifespan)

async def read_ultrasonic_sensor():
    """
    Function to reading data from an ultrasonic sensor
    """
    while True:
        await asyncio.sleep(0.25)  # Delay between readings
        distance = ultrasonic_sensor.get_distance()  # Distance measurement
        yield distance

@app.websocket("/ultrasonic_sensor")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def broadcast_sensor_data():
    """
    Background task to broadcast sensor data to all connected clients
    """
    async for distance in read_ultrasonic_sensor():
        if manager.has_active_connections():
            await manager.broadcast(str(distance))

# Optional endpoint to check if the server is running
@app.get("/")
async def read_root():
    return {"message": "FastAPI WebSocket server is running"}

if __name__ == "__main__":
    """
    Auto run server
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
