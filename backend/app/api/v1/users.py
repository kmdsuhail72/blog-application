from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate, UserCreatedResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()
auth_service = AuthService()

DB_SESSION = Depends(get_db)
CURRENT_USER_DEP = Depends(get_current_user)


@router.post("/", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = DB_SESSION):
    created_user = service.create_user(db, user)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    verification_token = auth_service.create_verification_token(created_user.email)
    return {
        "id": created_user.id,
        "name": created_user.name,
        "email": created_user.email,
        "is_verified": created_user.is_verified,
        "verification_token": verification_token,
    }


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user=CURRENT_USER_DEP,
    db: Session = DB_SESSION,
):
    return service.get_users(db)
