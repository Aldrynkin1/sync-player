from fastapi import FastAPI, WebSocket
from app.routes import RoomRout, UserRout
from app.core.database import init_db

app = FastAPI()


@app.on_event('startup')
def kaka():
    init_db()


@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(RoomRout)
app.include_router(UserRout)