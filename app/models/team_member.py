from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

team_members = Table(
    "team_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)