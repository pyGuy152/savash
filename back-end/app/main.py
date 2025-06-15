from typing import Optional
from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .routes import auth, users, classes, assignments, posts, games, submit, run, graphQL
from .oauth2 import get_current_user
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

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