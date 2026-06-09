from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from app.database import get_db
from app.models.team import Team
from app.models.user import User
from app.routes.auth import get_current_user
from app.schemas.team import TeamCreate
import uuid

team_router = APIRouter()

@team_router.post("/teams")
def create_team(team_data: TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.role == "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    if db.query(Team).filter(Team.name == team_data.name).first():
        raise HTTPException(status_code=400, detail="Team name already exists")


    new_team = Team(
        id=str(uuid.uuid4()),
        name=team_data.name,
        owner_id=current_user.id
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team

@team_router.get("/teams")
def get_teams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    teams = db.query(Team).filter(Team.members.any(id=current_user.id)).all()
    return teams    