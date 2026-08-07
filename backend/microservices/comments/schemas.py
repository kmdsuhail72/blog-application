from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    post_id: int = Field(..., example=1)
    author_id: int = Field(..., example=1)
    text: str = Field(..., min_length=1, max_length=500, example='Nice post!')


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=500, example='Updated comment text')


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
