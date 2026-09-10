import re

from sqlalchemy.orm import Session

from blog.models import Post


def generate_slug(title: str, db: Session) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")

    base_slug = slug
    counter = 2

    while db.query(Post).filter(Post.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug