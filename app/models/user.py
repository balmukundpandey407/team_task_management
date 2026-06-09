from sqlalchemy import Column,String
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.team_member import team_members

class User(Base):
    
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")
    teams = relationship("Team", secondary="team_members", back_populates="members")