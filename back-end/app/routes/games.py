import http
from typing import List, Optional
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random, time, json
from pydantic import BaseModel
from .. import oauth2
from ..schemas import games_schemas
from ..utils import sqlQuery
from datetime import datetime, timedelta, date

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
    if data.min:
        games[f"{code}"] = {"people":[],"time_end":datetime.now()+timedelta(minutes=data.min)}
    else:
        games[f"{code}"] = {"people":[],"time_end":None}
    return {"code":f"{code}","game":games[f"{code}"]}

class PlayerDataIn(BaseModel):
    name : str
    pos : List[int]

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

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
    
    async def close_connection(self, websocket: WebSocket, reason : Optional[str] = None):
        if reason:
            await websocket.close(reason=reason)
        else:
            await websocket.close(reason=reason)

manager = ConnectionManager()

@router.websocket("/{code}/{name}")
async def game(websocket: WebSocket,code: str, name: str):
    await manager.connect(websocket)
    try:
        try:
            for i in games[str(code)]["people"]:
                if i['name'] == name:
                    await manager.close_connection(websocket,reason=f"{name} is in game")
            games[str(code)]["people"].append({'name':f"{name}","pos":{"x":0,"y":0,"z":0},"rot":{"x":0,"y":0,"z":0},"points":0})
            await manager.send_message("Joined game",websocket)
        except:
            await manager.close_connection(websocket,reason="code not found")
        while True:
            jsonn = await manager.get_json(websocket)
            for i in range(len(games[str(code)]["people"])):
                if games[str(code)]["people"][i]["name"] == name:
                    games[str(code)]["people"][i]["pos"] = jsonn['pos']
                    games[str(code)]["people"][i]["rot"] = jsonn['rot']
            await manager.broadcast_json(json.dumps(games[str(code)], cls=DateTimeEncoder))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{name} left")
        for i in games[str(code)]["people"]:
            if i["name"] == name:
                games[str(code)]["people"].remove(i)
                break