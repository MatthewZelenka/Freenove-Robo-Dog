from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from .battery import battery
from ..connection_manager import ConnectionManager

router = APIRouter()

battery_SoC_manager = ConnectionManager()

battery_voltage_manager = ConnectionManager()

"""
battery voltage/SoC api
"""

batt = battery(bus=1, ref_voltage=5)

async def read_battery_voltage():
    """
    Function to reading voltage data from battery
    """
    while True:
        await asyncio.sleep(0.25)  # Delay between readings
        voltage = batt.voltage(channel=0)  # Voltage measurement
        yield voltage

async def read_SoC_voltage():
    """
    Function to reading SoC data from battery
    """
    while True:
        await asyncio.sleep(0.25)  # Delay between readings
        SoC = batt.SoC(channel=0)  # Distance measurement
        yield SoC

@router.websocket("/battery_voltage")
async def battery_voltage_websocket_endpoint(websocket: WebSocket):
    await battery_voltage_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await battery_voltage_manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        battery_voltage_manager.disconnect(websocket)

async def broadcast_battery_voltage_data():
    """
    Background task to broadcast sensor data to all connected clients
    """
    async for voltage in read_battery_voltage():
        if battery_voltage_manager.has_active_connections():
            await battery_voltage_manager.broadcast(str(voltage))

@router.websocket("/battery_SoC")
async def battery_SoC_websocket_endpoint(websocket: WebSocket):
    await battery_SoC_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await battery_SoC_manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        battery_SoC_manager.disconnect(websocket)

async def broadcast_battery_SoC_data():
    """
    Background task to broadcast sensor data to all connected clients
    """
    async for SoC in read_SoC_voltage():
        if battery_SoC_manager.has_active_connections():
            await battery_SoC_manager.broadcast(str(SoC))

