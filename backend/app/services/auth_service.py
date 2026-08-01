from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def authenticate_user(self, db, email: str, password: str):
        user = self.repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def create_token(self, email: str):
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        return create_access_token({"sub": email}, expires_delta=expires_delta)
