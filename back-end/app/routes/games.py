from typing import List, Optional, Dict
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random, time, json
from fastapi.websockets import WebSocketState
from pydantic import BaseModel
from .. import oauth2
from ..schemas import games_schemas
from ..sql_verification import getAssignmentType
from ..utils import sqlQuery
from datetime import datetime, timedelta, date

router = APIRouter(prefix='/games',tags=['Games'])

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
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self,code :str , websocket: WebSocket):
        await websocket.accept()
        if f"{code}" not in self.active_connections:
            self.active_connections[f"{code}"] = []
        self.active_connections[f"{code}"].append(websocket)
    
    def disconnect(self,code : str ,websocket: WebSocket):
        if f"{code}" in self.active_connections:
            self.active_connections[f"{code}"].remove(websocket)

    async def get_message(self, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            return await websocket.receive_text()

    async def get_json(self, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            return await websocket.receive_json()

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)
    
    async def send_json(self, json: dict, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_json(json)

    async def broadcast(self, code: str, message: str):
        for connection in self.active_connections[f"{code}"]:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_text(message)
    
    async def broadcast_json(self, code: str, json ):
        for connection in self.active_connections[f"{code}"]:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_json(json)
    
    async def close_connection(self, code: str, websocket: WebSocket, reason: Optional[str] = None):
        if websocket.application_state == WebSocketState.CONNECTED:
            try:
                if reason:
                    await websocket.close(code=status.WS_1001_GOING_AWAY, reason=reason)
                else:
                    await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
            except RuntimeError as e:
                print(f"Error closing WebSocket {websocket}: {e}")
            finally:
                self.disconnect(code, websocket)
        else:
            self.disconnect(code, websocket)
            print(f"Attempted to close already disconnected WebSocket: {websocket}")

games = {}
leaderboard = {}

@router.post("/")
def make_game(data:games_schemas.MakeGame):
    while True:
        code = random.randint(111111,999999)
        try:
            if not games[code]:
                break
        except:
            break
    if not data.days:
        data.days = 0
    if not data.hours:
        data.hours = 0
    if not data.min:
        data.min = 0
    if data.assignment_id and getAssignmentType(data.assignment_id) != "mcq" and getAssignmentType(data.assignment_id) != "tfq":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='you can only choose multiple choice and true false question assignments')
    games[f"{code}"] = {"people":[],"time_end":datetime.now()+timedelta(days=data.days,hours=data.hours,minutes=data.min),"assignment_id":data.assignment_id}
    leaderboard[str(code)] = []
    return {"code":f"{code}","game":games[f"{code}"]}

@router.get("/{code}/leaderboard")
def get_leaderboard(code: str):
    if code in leaderboard:
        return leaderboard[code]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with code {code} not found")

manager = ConnectionManager()

@router.websocket("/{code}/{name}")
async def game(websocket: WebSocket,code: str, name: str):
    await manager.connect(code, websocket)
    try:
        if str(code) not in games:
            await manager.close_connection(code,websocket,reason="code not found")
            print(f"WebSocket disconnected because code not found")
            return
        for i in games[str(code)]["people"]:
            if i['name'] == name:
                await manager.close_connection(code,websocket,reason=f"{name} is in game")
                print(f"WebSocket disconnected because {name} is in game")
                return
        games[str(code)]["people"].append({'name':f"{name}","pos":{"x":0,"y":0,"z":0},"rot":{"x":0,"y":0,"z":0},"vel":{"x":0,"y":0,"z":0},"points":0})
        leaderboard[str(code)].append({str(name):0})
        await manager.send_message("Joined game",websocket)
        while True:
            if datetime.now() > games[str(code)]["time_end"]:
                del games[str(code)]
                await manager.close_connection(code,websocket,reason=f"Game over")
                print(f"WebSocket disconnected because Game over")
                return
            jsonn = await manager.get_json(websocket)
            if jsonn:
                try:
                    if jsonn['message'] == 'question':
                        if (getAssignmentType(games[str(code)]['assignment_id'])=="mcq"):
                            data = sqlQuery('SELECT questions, choices, correct_answer FROM mcq WHERE assignment_id = %s;',(games[str(code)]['assignment_id'],))
                            index = random.randint(0,len(data['questions'])-1)
                            await manager.send_json({'question':data['questions'][index],'choices':data['choices'][index]},websocket)
                            answer_json = await manager.get_json(websocket)
                            if answer_json:
                                if answer_json["answer"] == data['correct_answer'][index]:
                                    await manager.send_json({'message':'Correct'},websocket)
                                else:
                                    await manager.send_json({'message':'Incorrect'},websocket)
                        else:
                            data = sqlQuery('SELECT questions, correct_answer FROM tfq WHERE assignment_id = %s;',(games[str(code)]['assignment_id'],))
                            index = random.randint(0,len(data['questions'])-1)
                            await manager.send_json({'question':data['questions'][index],'choices':['t','f']},websocket)
                            answer_json = await manager.get_json(websocket)
                            if answer_json:
                                if answer_json["answer"] == data['correct_answer'][index]:
                                    await manager.send_json({'message':'Correct'},websocket)
                                else:
                                    await manager.send_json({'message':'Incorrect'},websocket)
                except Exception as e:
                    print(e)
                    for i in range(len(games[str(code)]["people"])):
                        if games[str(code)]["people"][i]["name"] == name:
                            games[str(code)]["people"][i]["pos"] = jsonn['pos']
                            games[str(code)]["people"][i]["rot"] = jsonn['rot']
                            games[str(code)]["people"][i]["vel"] = jsonn['vel']
                await manager.broadcast_json(code,json.dumps(games[str(code)], cls=DateTimeEncoder))
    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected: {e.code} - {e.reason}")
        manager.disconnect(code, websocket)
        await manager.broadcast(code, f"{name} left")
        for i in games[str(code)]["people"]:
            if i["name"] == name:
                games[str(code)]["people"].remove(i)
                break
        if datetime.now() > games[str(code)]["time_end"]:
            del games[str(code)]
