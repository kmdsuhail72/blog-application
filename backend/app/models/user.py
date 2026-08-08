from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True)

    password = Column(String, nullable=False)

    is_verified = Column(Boolean, nullable=False, default=False)

    posts = relationship("Post", back_populates="author")
