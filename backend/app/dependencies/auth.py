from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


TOKEN_DEP = Depends(oauth2_scheme)
DB_DEP = Depends(get_db)


def get_current_user(
    token: str = TOKEN_DEP, db: Session = DB_DEP
) -> User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository().get_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


OPTIONAL_TOKEN_DEP = Depends(optional_oauth2_scheme)


def get_current_user_optional(
    token: str | None = OPTIONAL_TOKEN_DEP, db: Session = DB_DEP
) -> User | None:
    if token is None:
        return None

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str | None = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None

    return UserRepository().get_by_email(db, email)
