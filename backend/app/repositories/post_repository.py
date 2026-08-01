from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.post import Post
from app.models.tag import Tag


class PostRepository:
    def create(self, db: Session, post: Post) -> Post:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        search: str | None = None,
        category_slug: str | None = None,
        tag_name: str | None = None,
        author_id: int | None = None,
        published: bool | None = True,
    ):
        query = db.query(Post)

        if published is not None:
            query = query.filter(Post.published == published)

        if author_id is not None:
            query = query.filter(Post.author_id == author_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Post.title.ilike(search_term),
                    Post.content.ilike(search_term),
                )
            )

        if category_slug:
            query = query.join(Category).filter(
                func.lower(Category.slug) == category_slug.lower()
            )

        if tag_name:
            query = query.join(Post.tags).filter(
                func.lower(Tag.name) == tag_name.lower()
            )

        return query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

    def count(
        self,
        db: Session,
        search: str | None = None,
        category_slug: str | None = None,
        tag_name: str | None = None,
        author_id: int | None = None,
        published: bool | None = True,
    ) -> int:
        query = db.query(func.count(Post.id))

        if published is not None:
            query = query.filter(Post.published == published)

        if author_id is not None:
            query = query.filter(Post.author_id == author_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Post.title.ilike(search_term),
                    Post.content.ilike(search_term),
                )
            )

        if category_slug:
            query = query.join(Category).filter(
                func.lower(Category.slug) == category_slug.lower()
            )

        if tag_name:
            query = query.join(Post.tags).filter(
                func.lower(Tag.name) == tag_name.lower()
            )

        return query.scalar() or 0

    def get_by_id(self, db: Session, post_id: int) -> Post | None:
        return db.query(Post).filter(Post.id == post_id).first()

    def get_by_slug(self, db: Session, slug: str) -> Post | None:
        return db.query(Post).filter(Post.slug == slug).first()

    def delete(self, db: Session, post: Post) -> None:
        db.delete(post)
        db.commit()

    def get_or_create_tag(self, db: Session, tag_name: str) -> Tag:
        tag = db.query(Tag).filter(func.lower(Tag.name) == tag_name.lower()).first()
        if tag:
            return tag

        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
