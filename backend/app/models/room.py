from sqlalchemy import Column, String, Text, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.association import RoomMember

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    slug = Column(String(100), unique=True)
    description = Column(Text)
    name = Column(String)
    hashed_password = Column(String)
    current_time = Column(Float, default=0.0)
    video_url = Column(String)
    is_playing = Column(Boolean, default = False)
    
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='owned_rooms')
    
    members = relationship('User', secondary=RoomMember, back_populates='current_rooms')

    def __repr__(self):
        return f'Room with owner {self.owner} and name {self.name}'