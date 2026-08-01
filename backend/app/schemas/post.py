from datetime import datetime
from typing import List

from pydantic import BaseModel


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True,
    }


class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int
    published: bool = False
    cover_image: str | None = None
    tags: List[str] | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None
    published: bool | None = None
    cover_image: str | None = None
    tags: List[str] | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    published: bool
    cover_image: str | None = None
    author_id: int
    category_id: int
    tags: List[TagResponse] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }


class PostListResponse(BaseModel):
    page: int
    limit: int
    total: int
    items: List[PostResponse]
