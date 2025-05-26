from typing import List
from fastapi import APIRouter, WebSocketDisconnect, status, HTTPException, Depends, WebSocket
import random, time
from .. import oauth2
from ..schemas import games_schemas
from ..utils import sqlQuery

router = APIRouter(prefix='/games',tags=['Games'])

@router.get("/")
def test():
    return {'message':'hello'}