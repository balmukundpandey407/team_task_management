from sqlalchemy import Column,String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    team_id = Column(String, ForeignKey("teams.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
    team = relationship("Team", back_populates="tasks")

    
  