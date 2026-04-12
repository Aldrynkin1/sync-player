from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomCreate, RoomResponse
from typing import List
from app.schemas.room_members import RoomMemberResponse
from app.models import User, Room

class RoomService:
    def __init__(self, db: Session):
        self.repo = RoomRepository(db)
        self.db = db


    def create_room(self, room_data: RoomCreate) -> RoomResponse:
        room = self.repo.create_room(room_data)
        return RoomResponse.model_validate(room)

    def get_room(self, room_id: int) -> RoomResponse:
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
    
    def add_user_to_room(self, room_id: int, user: User) -> Room:
        room = self.repo.get_room_by_id(room_id)

        if not room:
            return None
        
        if user not in room.members:
            room.members.append(user)
            self.db.commit()
            self.db.refresh(room)

        return room
    
    def get_all_rooms(self) -> List[RoomResponse]:
        rooms = self.repo.get_all_rooms()
        
        return [RoomResponse.model_validate(room) for room in rooms]