from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.schemas.auth import Token, VerifyEmailRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

OAUTH2_PASSWORD_FORM = Depends(OAuth2PasswordRequestForm)
CURRENT_USER = Depends(get_current_user)
DB_SESSION = Depends(get_db)

router = APIRouter(prefix="/auth", tags=["Auth"])

service = AuthService()


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = OAUTH2_PASSWORD_FORM,
    db: Session = DB_SESSION,
):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if user == "unverified":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email address has not been verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = service.create_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify")
def verify_email(
    request: VerifyEmailRequest,
    db: Session = DB_SESSION,
):
    user = service.verify_email_token(db, request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )
    return {"message": "Email verified successfully"}


CURRENT_USER_DEP = Depends(get_current_user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=CURRENT_USER_DEP):
    return current_user
