from sqlalchemy import Table, Column, ForeignKey, String
from app.core.database import Base

class RoomMember(Base):
    __tablename__ = 'room_members'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    room_id = Column(ForeignKey('rooms.id'), primary_key=True)
    role = Column(String, default="guest") 