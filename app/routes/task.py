from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.models.team import Team
from app.models.user import User
from app.security import decode_jwt
from app.routes.auth import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate
import uuid

task_router = APIRouter()

@task_router.post("/tasks")
def create_task(task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Check if team exists
    team = db.query(Team).filter(Team.id == task_data.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if user is a member of the team
    if current_user.id not in [member.id for member in team.members]:
        raise HTTPException(status_code=403, detail="You are not a member of this team")

    new_task = Task(
        id=str(uuid.uuid4()),
        title=task_data.title,
        description=task_data.description,
        status="active",
        assigned_to=task_data.assigned_to,
        team_id=task_data.team_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@task_router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Get all teams the user is a member of
    teams = db.query(Team).filter(Team.members.any(id=current_user.id)).all()

    # Get all tasks for those teams
    tasks = []
    for team in teams:
        team_tasks = db.query(Task).filter(Task.team_id == team.id).all()
        tasks.extend(team_tasks)

    return tasks    

@task_router.put("/tasks/{id}")
def update_task(id: str, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if user is the owner of the task or a member of the team
    if task.assigned_to != current_user.id and current_user.id not in [member.id for member in task.team.members]:
        raise HTTPException(status_code=403, detail="You do not have permission to update this task")

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.assigned_to = task_data.assigned_to
    task.team_id = task_data.team_id
    db.commit()
    db.refresh(task)

    return task

@task_router.delete("/tasks/{id}")
def delete_task(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if user is the owner of the task or a member of the team
    if task.assigned_to != current_user.id and current_user.id not in [member.id for member in task.team.members]:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this task")

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted successfully"}