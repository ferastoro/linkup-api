from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    full_name = Column(String)
    age = Column(Integer)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    interests = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())