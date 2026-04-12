from sqlalchemy import Table, Column, ForeignKey
from app.core.database import Base

room_members = Table(
    'room_members',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('room_id', ForeignKey('rooms.id'), primary_key=True)
)