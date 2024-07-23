import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except asyncio.exceptions.CancelledError:
            pass

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except asyncio.exceptions.CancelledError:
                pass

    async def broadcast_bytes(self, message: bytes):
        for connection in self.active_connections:
            try:
                await connection.send_bytes(message)
            except asyncio.exceptions.CancelledError:
                pass
    
    def has_active_connections(self) -> bool:
        return len(self.active_connections) > 0
