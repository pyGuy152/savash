from typing import List
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random, time
from .. import oauth2
from ..schemas import games_schemas
from ..utils import sqlQuery

router = APIRouter(prefix='/games',tags=['Games'])

class game():
    name: str
    time: str
    host: str
    people: list
    def __init__(self, name, min, people, host_name):
        self.name = name
        self.time = min
        self.host = host_name
        self.people = people

games = {}
questions = [{'q':'What is 1+1','choices':['0','2','11','Window'],'answer':'2'}]

def checkCode(code):
    try:
        games[code] = games[code]
        return True
    except:
        return False

@router.post("/")
def make_game(data:games_schemas.MakeGame):
    code = random.randint(10000,99999)
    while checkCode(code):
        code = random.randint(10000,99999)
    games[code] = game(data.name, data.min, [], data.host_name)
    return code


@router.websocket("/{code}")
async def websocket(code:int ,websocket: WebSocket):
    await websocket.accept()
    try:
        try:
            game = games[code]
        except:
            if (websocket):
                await websocket.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='code does not exist')
        
        data = await websocket.receive_text()
        print(f"Received: {data}")
        game.people.append(data)
        for question in questions:
            await websocket.send_text(question['q'])
            await websocket.send_text(question['choices'][0]+" "+question['choices'][1]+" "+question['choices'][2]+" "+question['choices'][3])
            answer = await websocket.receive_text()
            if answer == question['answer']:
                await websocket.send_text("Correct")
            else:
                await websocket.send_text("Incorrect")
        await websocket.close()
    except WebSocketDisconnect:
        print("Client disconnected")
