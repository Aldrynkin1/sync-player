from sqlalchemy.orm import Session
from typing import Optional
from slugify import slugify
import uuid
from typing import List

from app.models.room import Room
from app.schemas.room import RoomCreate
from app.core.auth import hash_password

import uuid
from slugify import slugify
from sqlalchemy.orm import Session
from app.schemas.room import RoomResponse

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, room_data: RoomCreate, owner_id: int) -> Room:
        data = room_data.model_dump()
        password = data.pop("password", None) # Безопасно извлекаем пароль

        # Создаем чистый слаг из названия
        base_slug = slugify(data["name"])
        
        # Добавляем короткий UUID для уникальности
        slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        db_room = Room(
            **data,
            slug=slug,
            hashed_password=hash_password(password) if password else None,
            current_time=0.0,
            is_playing=False,
        )

        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def get_all_rooms(self) -> List[RoomResponse]:
        rooms = self.db.query(Room).all()

        if not rooms:
            return []
        
        return [RoomResponse.model_validate(room) for room in rooms]
    
    def delete_room(self, room_id: int) -> bool:
        room = self.db.query(Room).filter(Room.id == room_id).first()

        if not room:
            return False
        
        self.db.delete(room)
        self.db.commit()
        return True
    
    def new_video(self, room_id: int, video_url: str):
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return False
        
        room.video_url = video_url
        
        return room