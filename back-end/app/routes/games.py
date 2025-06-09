import http
from typing import List
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
        games[f"{code}"] = {"people":[{'name':f"{data.host_name}","pos":[0,0,0],"points":0}],"time_end":datetime.now()+timedelta(minutes=data.min)}
    else:
        games[f"{code}"] = {"people":[{'name':f"{data.host_name}","pos":[0,0,0],"points":0}],"time_end":None}
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
                games[str(code)]["people"].append({'name':f"{name}","pos":[0,0,0],"points":0})
                await manager.send_message("Joined game",websocket)
                break
            else:
                await manager.send_message("code not found, try again",websocket)
        while True:
            jsonn = await manager.get_json(websocket)
            for i in range(len(games[str(code)]["people"])):
                if games[str(code)]["people"][i]["name"] == jsonn['name']:
                    games[str(code)]["people"][i]["pos"] = jsonn['pos']
                    games[str(code)]["people"][i]["points"] = jsonn['points']
            await manager.broadcast_json(json.dumps(games[str(code)], cls=DateTimeEncoder))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{name} left")
        for i in games[str(code)]["people"]:
            if i["name"] == name:
                games[str(code)]["people"].remove(i)
                break