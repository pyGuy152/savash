from fastapi import FastAPI
from .routes import auth, users, classes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'https://savash.rohanjain.xyz',
    'https://builds.rohanjain.xyz',
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

@app.get("/")
def root():
    return {'message':'hello people of the world'}

