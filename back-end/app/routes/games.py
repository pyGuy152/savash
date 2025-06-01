import http
from typing import List
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random, time
from pydantic import BaseModel
from .. import oauth2
from ..schemas import games_schemas
from ..utils import sqlQuery
from datetime import datetime, timedelta

router = APIRouter(prefix='/games',tags=['Games'])

games = {}

@router.post("/")
def make_game(data:games_schemas.MakeGame):
    while True:
        code = random.randint(111111,999999)
        try:
            if not games[code]:
                break
        except:
            break
    games[f"{code}"] = {"people":[{'name':f"{data.host_name}","pos":[0,0,0]}],"time_end":datetime.now()+timedelta(minutes=data.min)}
    return games

class PlayerDataIn(BaseModel):
    name : str
    pos : List[int]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def get_message(self, websocket: WebSocket):
        return await websocket.receive_text()

    async def get_json(self, websocket: WebSocket):
        return await websocket.receive_json()

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def broadcast_json(self, json):
        for connection in self.active_connections:
            await connection.send_json(json)

manager = ConnectionManager()

@router.websocket("/{name}")
async def game(websocket: WebSocket, name: str):
    await manager.connect(websocket)
    try:
        while True:
            await manager.send_message("Send game code: ",websocket)
            code = await manager.get_message(websocket)
            if games[str(code)]:
                for i in games[str(code)]["people"]:
                    if i['name'] == name:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{name} is in game")
                games[str(code)]["people"].append({'name':f"{name}","pos":[0,0,0]})
                await manager.send_message("Joined game",websocket)
                break
            else:
                await manager.send_message("code not found, try again",websocket)
        while True:
            try:
                json = await manager.get_json(websocket)
                json = PlayerDataIn(**json)
                for i in range(len(games[str(code)]["people"])):
                    if games[str(code)]["people"][i]["name"] == json.name:
                        games[str(code)]["people"][i]["pos"] = json.pos
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Make sure you are sending json in this format {"name":name,"pos":[0,0,0]}')
            await manager.broadcast_json(games[str(code)])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{name} left")
        for i in games[str(code)]["people"]:
            if i["name"] == name:
                games[str(code)]["people"].remove(i)
                break