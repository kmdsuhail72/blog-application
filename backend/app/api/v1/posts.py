from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user, get_current_user_optional
from app.schemas.post import PostCreate, PostListResponse, PostResponse, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])

service = PostService()

CURRENT_USER_OPTIONAL_DEP = Depends(get_current_user_optional)
CURRENT_USER_DEP = Depends(get_current_user)
DB_SESSION = Depends(get_db)


@router.get("/", response_model=PostListResponse)
def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    category: str | None = Query(None),
    tag: str | None = Query(None),
    mine: bool = Query(False),
    current_user= CURRENT_USER_OPTIONAL_DEP,
    db: Session = DB_SESSION,
):
    if mine and current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to view your drafts",
        )

    return service.get_posts(
        db,
        page=page,
        limit=limit,
        search=search,
        category=category,
        tag=tag,
        mine=mine,
        current_user_id=current_user.id if current_user else None,
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    current_user= CURRENT_USER_OPTIONAL_DEP,
    db: Session = DB_SESSION,
):
    post = service.get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if not post.published and (
        current_user is None or post.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    current_user=CURRENT_USER_DEP,
    db: Session = DB_SESSION,
):
    post = service.create_post(db, current_user.id, post_data)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category"
        )
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user= CURRENT_USER_DEP,
    db: Session = DB_SESSION,
):
    post = service.get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    updated = service.update_post(db, post, post_data)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category"
        )
    return updated


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user= CURRENT_USER_DEP, db: Session = DB_SESSION):
    post = service.get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    service.delete_post(db, post)
