from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from .routes import auth, users, classes, assignments, posts, games, submit, run
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    'https://savash.rohanjain.xyz',
    'https://builds.rohanjain.xyz',
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

@app.get('/')
def root():
    return RedirectResponse('https://savash.rohanjain.xyz')