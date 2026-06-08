from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.task import Task
from app.routes.auth import get_current_user
from app.security import decode_jwt

admin_router = APIRouter()

@admin_router.get("/admin/users")
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Check if the current user is an admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    users = db.query(User).all()
    return users

@admin_router.get("/admin/tasks")
def get_all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Check if the current user is an admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    tasks = db.query(Task).all()
    return tasks