from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.auth import hash_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_user(self, user_data: UserCreate):
        data = user_data.model_dump()
        password = data.pop('password')
        data['hashed_password'] = hash_password(password)
        
        db_user = User(**data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self):
        return self.db.query(User).all()