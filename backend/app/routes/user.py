from fastapi import APIRouter, status, Depends
from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomResponse, RoomCreate
from app.schemas.user import UserResponse
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate
rout = APIRouter(
    prefix='/users',
    tags=['users']
)

@rout.get('/', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    
    serv = UserService(db)
    users = serv.get_all_users()
    return users

@rout.post('/create', status_code=status.HTTP_200_OK)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> None:
    serv = UserService(db)
    
    return serv.create_user(user_data)

@rout.post('/join/{user_id}')
def join_to_room(user_id, room_id, db: Session = Depends(get_db)):
    serv = UserService(db)
    return serv.join_to_room(room_id, user_id)