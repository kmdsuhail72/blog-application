from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db, user_data: UserCreate):
        existing_user = self.repository.get_by_email(db, user_data.email)
        if existing_user:
            return None

        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_data.password)

        user = User(**user_dict)
        return self.repository.create(db, user)

    def get_users(self, db):
        return self.repository.get_all(db)
