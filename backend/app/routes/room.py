from fastapi import APIRouter, status, Depends
from app.models.user import User
from app.schemas.room import RoomResponse, RoomCreate
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.room_service import RoomService
from app.services.user_service import UserService
from fastapi import HTTPException
from app.schemas.user import UserResponse


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
def create_room(room_data: RoomCreate, owner_id: int,  db: Session = Depends(get_db)) -> None:
    serv = RoomService(db)
    
    return serv.create_room(room_data, owner_id)

@rout.get('/{id}')
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

@rout.delete('/delete/{room_id}')
def delete_room(room_id: int, user_id: int, db: Session = Depends(get_db)):
    serv = RoomService(db)
    
    if not serv.delete_room(room_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Room not found')
    
    

    return {'status': 'success', 'message': 'Room deleted'}