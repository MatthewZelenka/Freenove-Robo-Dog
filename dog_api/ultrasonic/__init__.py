from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import RPi.GPIO as GPIO
import asyncio

from .RPi_ultrasonic import ultrasonic
from ..connection_manager import ConnectionManager

router = APIRouter()

ultrasonic_manager = ConnectionManager()

"""
Ultrasonic sensor api
"""

ultrasonic_sensor = ultrasonic(trigger_pin=27, echo_pin=22, GPIO_Mode=GPIO.BCM)

async def read_ultrasonic_sensor(ultrasonic_sensor: ultrasonic):
    """
    Function to reading data from an ultrasonic sensor
    """
    while True:
        await asyncio.sleep(0.25)  # Delay between readings
        distance = ultrasonic_sensor.get_distance()  # Distance measurement
        yield distance

@router.websocket("/ultrasonic_sensor")
async def ultrasonic_websocket_endpoint(websocket: WebSocket):
    await ultrasonic_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ultrasonic_manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        ultrasonic_manager.disconnect(websocket)

async def broadcast_ultrasonic_sensor_data():
    """
    Background task to broadcast sensor data to all connected clients
    """
    while True:
        if ultrasonic_manager.has_active_connections():
            async for distance in read_ultrasonic_sensor(ultrasonic_sensor):
                if ultrasonic_manager.has_active_connections():
                    await ultrasonic_manager.broadcast(str(distance))
                else:
                    break
        else:
            await asyncio.sleep(1)  # Check for active connections periodically
