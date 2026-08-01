import re
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate


def make_slug(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug


class PostService:
    def __init__(self):
        self.repository = PostRepository()

    def _build_tags(self, db: Session, tag_names: list[str] | None):
        tags: list[Tag] = []
        if not tag_names:
            return tags

        for name in tag_names:
            normalized = name.strip()
            if not normalized:
                continue
            tags.append(self.repository.get_or_create_tag(db, normalized))

        return tags

    def _generate_unique_slug(self, db: Session, title: str) -> str:
        base_slug = make_slug(title)
        slug = base_slug
        index = 1
        while self.repository.get_by_slug(db, slug) is not None:
            slug = f"{base_slug}-{index}"
            index += 1
        return slug

    def create_post(self, db: Session, author_id: int, post_data: PostCreate) -> Post:
        category = (
            db.query(Category).filter(Category.id == post_data.category_id).first()
        )
        if category is None:
            return None

        slug = self._generate_unique_slug(db, post_data.title)
        tags = self._build_tags(db, post_data.tags)

        post = Post(
            title=post_data.title,
            slug=slug,
            content=post_data.content,
            cover_image=post_data.cover_image,
            published=post_data.published,
            author_id=author_id,
            category_id=post_data.category_id,
            tags=tags,
        )
        return self.repository.create(db, post)

    def get_posts(
        self,
        db: Session,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        mine: bool = False,
        current_user_id: int | None = None,
    ):
        skip = (page - 1) * limit
        author_id = current_user_id if mine else None
        published = None if mine and current_user_id is not None else True

        items = self.repository.get_all(
            db,
            skip=skip,
            limit=limit,
            search=search,
            category_slug=category,
            tag_name=tag,
            author_id=author_id,
            published=published,
        )
        total = self.repository.count(
            db,
            search=search,
            category_slug=category,
            tag_name=tag,
            author_id=author_id,
            published=published,
        )
        return {
            "page": page,
            "limit": limit,
            "total": total,
            "items": items,
        }

    def get_post(self, db: Session, post_id: int) -> Post | None:
        return self.repository.get_by_id(db, post_id)

    def update_post(self, db: Session, post: Post, post_data: PostUpdate) -> Post:
        if post_data.title is not None and post.title != post_data.title:
            post.slug = self._generate_unique_slug(db, post_data.title)
            post.title = post_data.title

        if post_data.content is not None:
            post.content = post_data.content

        if post_data.cover_image is not None:
            post.cover_image = post_data.cover_image

        if post_data.category_id is not None:
            category = (
                db.query(Category).filter(Category.id == post_data.category_id).first()
            )
            if category is None:
                return None
            post.category_id = post_data.category_id

        if post_data.published is not None:
            post.published = post_data.published

        if post_data.tags is not None:
            post.tags = self._build_tags(db, post_data.tags)

        db.commit()
        db.refresh(post)
        return post

    def delete_post(self, db: Session, post: Post) -> None:
        self.repository.delete(db, post)
