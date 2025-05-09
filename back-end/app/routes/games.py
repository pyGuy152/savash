from typing import List
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random
from .. import oauth2
from ..schemas import games_schemas
from ..utils import sqlQuery

router = APIRouter(prefix='/games',tags=['Games'])

class game():
    name: str
    time: str
    def __init__(self, name, min):
        self.name = name
        self.time = min

games = {}

@router.post("/")
def make_game(data:games_schemas.MakeGame):
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
    x = random.randint(10000,99999)
    games[x] = game(data.name, data.min)
    return x


@router.websocket("/{code}")
async def websocket(code:int ,websocket: WebSocket):
    await websocket.accept()
    try:
        game = games[code]
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            await websocket.send_text(str(game.time))
            if data == "close":
                games[code] = None
                await websocket.close()
                break
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
