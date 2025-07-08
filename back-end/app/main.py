from typing import Optional
from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .routes import auth, users, classes, assignments, posts, games, submit, run, graphQL
from .oauth2 import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from .utils import sqlQuery
app = FastAPI()

# Setup db - runs only once at startup
@app.on_event("startup")
async def startup_event():
    sqlQuery('CREATE TABLE IF NOT EXISTS class (code INTEGER PRIMARY KEY, name VARCHAR NOT NULL, created_at DATE DEFAULT CURRENT_DATE, owner INTEGER NOT NULL);',(),fetchNone=True)
    sqlQuery('CREATE TABLE IF NOT EXISTS coding (assignment_id INTEGER PRIMARY KEY, title VARCHAR, description VARCHAR, due_date DATE, points INTEGER, code_file VARCHAR, input VARCHAR[][], output VARCHAR[], created_at TIMESTAMPTZ DEFAULT NOW(), code INTEGER, FOREIGN KEY (code) REFERENCES class(code) ON DELETE CASCADE);',(),fetchNone=True)
    sqlQuery('CREATE TABLE IF NOT EXISTS frq ();',(),fetchNone=True)

origins = [
    'https://savash.rohanjain.xyz',
    'https://builds.rohanjain.xyz',
    'https://savashkart.rohanjain.xyz',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(assignments.router)
app.include_router(submit.router)
app.include_router(posts.router)
app.include_router(run.router)
app.include_router(games.router)
#dependencies=[Depends(get_current_user)]
app.include_router(graphQL.router)

@app.get('/')
def root():
    return RedirectResponse('https://savash.rohanjain.xyz')

@app.post("/email")
async def receive_raw_email(request: Request):
    body = await request.body()
    import email
    msg = email.message_from_bytes(body)
    print(str(msg).split(";"))
    for i in str(msg).split(";"):
        if '"to":' in i:
            print(i)
    return {"status": "parsed raw email"}
