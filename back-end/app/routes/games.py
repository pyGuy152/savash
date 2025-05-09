from typing import List
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random
from .. import oauth2
from ..schemas import classes_schemas
from ..utils import sqlQuery

router = APIRouter(prefix='/games',tags=['Games'])

class game():
    j : str


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            if data == "close":
                await websocket.close()
                break
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
