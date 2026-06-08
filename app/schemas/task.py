from pydantic import BaseModel
from typing import Union, Optional  

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    team_id: str

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str

