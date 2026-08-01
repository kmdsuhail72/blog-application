from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from app.db.database import Base


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
