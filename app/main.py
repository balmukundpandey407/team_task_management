from fastapi import FastAPI
from .routes.task import task_router
from .routes.auth import auth_router
from .routes.team import team_router
from .routes.admin import admin_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Team Task Management API!"}


app.include_router(auth_router,tags=["AUTHENTICATION_ROUTES"])
app.include_router(task_router,tags=["TASK_ROUTES"])
app.include_router(team_router,tags=["TEAM_ROUTES"])
app.include_router(admin_router,tags=["ADMIN_ROUTES"])
