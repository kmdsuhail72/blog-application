from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token, decode_token, verify_password
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
        if not user.is_verified:
            return "unverified"
        return user

    def create_token(self, email: str):
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        return create_access_token({"sub": email}, expires_delta=expires_delta)

    def create_verification_token(self, email: str):
        expires_delta = timedelta(minutes=settings.verification_token_expire_minutes)
        return create_access_token(
            {"sub": email, "type": "email_verification"},
            expires_delta=expires_delta,
        )

    def verify_email_token(self, db, token: str):
        payload = decode_token(token)
        if not payload or payload.get("type") != "email_verification":
            return None
        email = payload.get("sub")
        if not email:
            return None

        user = self.repository.get_by_email(db, email)
        if not user or user.is_verified:
            return None

        user.is_verified = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
