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
    people = []
    def __init__(self, name, min):
        self.name = name
        self.time = min

games = {}

@router.post("/")
def make_game(data:games_schemas.MakeGame):
    x = random.randint(10000,99999)
    games[x] = game(data.name, data.min)
    return x


@router.websocket("/{name}/{code}")
async def websocket(name:str, code:int ,websocket: WebSocket):
    await websocket.accept()
    try:
        try:
            games[code].people.append(name)
            game = games[code]
        except:
            if (websocket):
                await websocket.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='code does not exist')
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            if data == "end":
                del games[code]
                await websocket.send_text("closing")
                await websocket.close()
                break
            await websocket.send_text(f"name: {game.name}, time: {game.time}, people: {game.people}")
    except WebSocketDisconnect:
        print("Client disconnected")
