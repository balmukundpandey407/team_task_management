from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy.orm import Session
import uuid

from app.schemas.user import UserCreate, Userout, UserLogin, UserToken
from app.models.user import User, Base
from app.database import get_db, engine
from app.security import security, verify_password, hash_password, sign_jwt, decode_jwt

auth_router = APIRouter()
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

# Create all tables in the database
Base.metadata.create_all(bind=engine)


@auth_router.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(FRONTEND_DIR / "login.html")


@auth_router.get("/register", include_in_schema=False)
def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")

@auth_router.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


@auth_router.get("/frontend/{file_path:path}", include_in_schema=False)
def frontend_file(file_path: str):
    requested_file = (FRONTEND_DIR / file_path).resolve()
    if not requested_file.is_relative_to(FRONTEND_DIR) or not requested_file.is_file():
        raise HTTPException(status_code=404, detail="Frontend file not found")
    return FileResponse(requested_file)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    decoded_token = decode_jwt(token)

    if not decoded_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == decoded_token["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        email=user.email
    )


@auth_router.post("/register")
def sign_up_user(sign_up_data: UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == sign_up_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists please login instead")

    # Hash the password
    hashed_password = hash_password(sign_up_data.password)
    
    new_user = User(
     id= str(uuid.uuid4()),
     first_name=sign_up_data.first_name,
     last_name=sign_up_data.last_name,
     role="member",
     email=sign_up_data.email,
     password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@auth_router.post("/login",response_model=UserToken)
def login_user(login_data: UserLogin, db: Session = Depends(get_db), ):
    # Find the user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate a JWT token
    token = sign_jwt(user.id)
    if not token:
        raise HTTPException(status_code=500, detail="Token generation failed")
    return UserToken(token=token)
