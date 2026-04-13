from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.association import RoomMember

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String, unique=True)
    description = Column(Text)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    avatar = Column(String)
    in_room_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default='guest')
    
    current_rooms = relationship('Room', secondary=RoomMember, back_populates='members')
    
    owned_rooms = relationship('Room', back_populates='owner', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Profile {self.username} in room {self.in_room_name}'