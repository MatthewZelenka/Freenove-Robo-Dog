from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from .connection_manager import ConnectionManager
from . import ultrasonic
from . import analog_digital_converter
from . import camera

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
    asyncio.create_task(ultrasonic.broadcast_ultrasonic_sensor_data())
    
    asyncio.create_task(analog_digital_converter.broadcast_battery_voltage_data())
    asyncio.create_task(analog_digital_converter.broadcast_battery_SoC_data())
    
    asyncio.create_task(camera.broadcast_camera_data())
    yield
    # On death
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(ultrasonic.router)

app.include_router(analog_digital_converter.router)

# Optional endpoint to check if the server is running
@app.get("/")
async def read_root():
    return {"message": "FastAPI WebSocket server is running"}

