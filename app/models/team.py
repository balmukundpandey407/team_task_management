from sqlalchemy import Column,String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Team(Base):
    
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)

    members = relationship("User", secondary="team_members", back_populates="teams")
    tasks = relationship("Task", back_populates="team")

  