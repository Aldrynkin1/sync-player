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

@rout.get('/room', response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
def get_all_rooms(db: Session = Depends(get_db)):
    
    serv = RoomService(db)
    rooms = serv.get_all_rooms()
    return rooms

@rout.post('/room/create', status_code=status.HTTP_200_OK)
def create_room(room_data: RoomCreate, db: Session = Depends(get_db)) -> None:
    serv = RoomService(db)
    
    return serv.create_room(room_data)

@rout.get('/room/{id}')
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    serv = RoomService(db)

    return serv.get_room_by_id(room_id)

@rout.post('/members/add/{user_id}', response_model=RoomResponse)
def add_user_to_room(user_id: int, room_id: int, db: Session = Depends(get_db)):
    serv = RoomService(db)
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail='User not found')
    
    return serv.add_user_to_room(room_id, user_id)