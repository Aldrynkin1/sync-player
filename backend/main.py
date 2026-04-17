from fastapi import FastAPI, WebSocket
from app.routes import RoomRout, UserRout
from app.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import settings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.cors_origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def kaka():
    init_db()

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(RoomRout)
app.include_router(UserRout)