from sqlalchemy.orm import Session
from typing import Optional
from slugify import slugify
import uuid

from app.models.room import Room
from app.schemas.room import RoomCreate
from app.core.auth import hash_password


import uuid
from slugify import slugify  # Импорт из python-slugify
from sqlalchemy.orm import Session
# Импортируйте ваши модели и схемы (Room, RoomCreate, hash_password)

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, room_data: RoomCreate) -> Room:
        data = room_data.model_dump()
        password = data.pop("password", None) # Безопасно извлекаем пароль

        # Создаем чистый слаг из названия (поддерживает кириллицу)
        base_slug = slugify(data["name"])
        
        # Добавляем короткий UUID для уникальности, как у вас и было
        slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        db_room = Room(
            **data,
            slug=slug,
            hashed_password=hash_password(password) if password else None,
            current_time=0.0,
            is_playing=False
        )

        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def get_all_rooms(self):
        return self.db.query(Room).all()