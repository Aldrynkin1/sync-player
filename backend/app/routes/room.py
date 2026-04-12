from fastapi import APIRouter, status, Depends
from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomResponse, RoomCreate
from app.schemas.user import UserResponse
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.room_service import RoomService

rout = APIRouter(
    prefix='/room',
    tags=['rooms']
)

@rout.get('/', response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
def get_all_rooms(db: Session = Depends(get_db)):
    
    serv = RoomService(db)
    rooms = serv.get_all_rooms()
    return rooms

@rout.post('/create', status_code=status.HTTP_200_OK)
def create_room(room_data: RoomCreate, db: Session = Depends(get_db)) -> None:
    serv = RoomService(db)
    
    return serv.create_room(room_data)