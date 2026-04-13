from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from app.services.room_service import RoomService
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from typing import List

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)
        self.room_serv = RoomService(db)
        
    def join_to_room(self, room_id: int, user_id: int):
        room = self.room_serv.get_room_by_id(room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail='Room not found')
        
        user = self.repo.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        
        self.room_serv.add_user_to_room(room_id, user)
        return {'detail': f'User {user.username} added to room {room_id}'}
    
    def get_all_users(self) -> List[User]:
        users = self.repo.get_all_users()
        
        return [UserResponse.model_validate(u) for u in users]
    
    def create_user(self, user_data: UserCreate) -> User:
        return self.repo.create_user(user_data)
    
    def get_user_by_id(self, user_id: int):
        repo = self.repo.get_user_by_id(user_id)
        return repo
    
    def delete_user(self, user_id: int):
        return self.repo.delete_user(user_id)