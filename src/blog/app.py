from blog.db import get_db
from blog.models import Post
from blog.schemas import PostCreate, PostResponse, PostUpdate
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from blog.utils import generate_slug
from blog.auth import get_current_user, require_admin

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/posts", response_model=list[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    return (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.get("/posts/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts", response_model=PostResponse)
def create_post(
    post: PostCreate, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    new_post = Post(
        title=post.title,
        slug=generate_slug(post.title, db),
        content=post.content,
        image_url=post.image_url,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.patch("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: UUID,
    post: PostUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_post, field, value)

    db.commit()
    db.refresh(existing_post)

    return existing_post


@app.delete("/posts/{post_id}")
def delete_post(
    post_id: UUID, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}
