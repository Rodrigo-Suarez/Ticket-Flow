from sqlalchemy import TIMESTAMP, Integer, Column, String, Enum, func
from src.database.db import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)  
    username = Column(String(50), nullable=False, unique=True)  
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)  
    role = Column(Enum("administrador", "asistente"), nullable=False)  
    creation_date = Column(TIMESTAMP, default=func.now()) 