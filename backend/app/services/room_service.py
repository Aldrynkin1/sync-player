from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomCreate, RoomResponse
from typing import List
from app.schemas.room_members import RoomMemberResponse
from app.models.room import Room
from app.repositories.user_repository import UserRepository

class RoomService:
    def __init__(self, db: Session):
        self.repo = RoomRepository(db)
        self.db = db
        self.user_repo = UserRepository(db)


    def create_room(self, room_data: RoomCreate, owner_id: int) -> RoomResponse:
        room = self.repo.create_room(room_data, owner_id)
        return RoomResponse.model_validate(room)

    def get_room_by_id(self, room_id: int) -> RoomResponse:
        room = self.repo.get_room_by_id(room_id)

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        return RoomResponse.model_validate(room)
    
    def get_members(self, room_id: int) -> List[RoomMemberResponse]:
        room = self.repo.get_room_by_id(room_id)

        if not room:
            raise HTTPException(status_code=404, detail='Room not found')

        return [RoomMemberResponse.model_validate(u) for u in room.members]
    
    def add_user_to_room(self, room_id: int, user_id: int) -> Room:
        room = self.repo.get_room_by_id(room_id)
        user = self.user_repo.get_user_by_id(user_id)
        
        if not room or not user:
            raise HTTPException(status_code=404, detail='Room or user not found')

        if not user in room.members:
            room.members.append(user)
            self.db.commit()
            self.db.refresh(room)
        
        return RoomResponse.model_validate(room)
    
    def get_all_rooms(self) -> List[RoomResponse]:
        rooms = self.repo.get_all_rooms()
        
        return [RoomResponse.model_validate(room) for room in rooms]
    
    def delete_room(self, room_id: int):
        room = self.repo.get_room_by_id(room_id)

        if not room:
            raise HTTPException(status_code=404, detail='Room not found')

        return self.repo.delete_room(room_id)
    
    def update_room_state(self, room_id: int, time: float, is_playing: bool):
        room = self.repo.get_room_by_id(room_id)
        
        if room:
            room.current_time = time
            room.is_playing = is_playing
            self.db.commit()
            self.db.refresh(room)
        return room
    
    def new_video(self, room_id: int, video_url: str, user_id: int):
        room = self.repo.get_room_by_id(room_id)

        if not room:
            return False
        
        if user_id != room.owner_id:
            raise HTTPException(status_code=401, detail='Only owner can change video')
        
        if room:
            room.video_url = video_url
            self.db.commit()

        return room
    
    def get_room_by_name(self, room_name: str):
        room = self.repo.get_room_by_name(room_name)

        if not room:
            raise HTTPException(status_code=404, detail='Room not found')

        return room