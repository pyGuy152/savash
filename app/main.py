from fastapi import FastAPI
from .routes import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {'message':'hello people of the world'}