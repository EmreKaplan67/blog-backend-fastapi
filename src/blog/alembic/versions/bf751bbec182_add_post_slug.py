"""add post slug

Revision ID: bf751bbec182
Revises: 303842f8676c
Create Date: 2026-09-06 12:02:11.704614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf751bbec182'
down_revision: Union[str, Sequence[str], None] = '303842f8676c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the column temporarily as nullable
    op.add_column(
        "posts",
        sa.Column("slug", sa.String(length=255), nullable=True),
    )

    # 2. Generate slugs for existing posts
    connection = op.get_bind()

    posts = connection.execute(
        sa.text("SELECT id, title FROM posts")
    ).fetchall()

    import re

    for post_id, title in posts:
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")

        connection.execute(
            sa.text(
                "UPDATE posts SET slug = :slug WHERE id = :id"
            ),
            {"slug": slug, "id": post_id},
        )

    # 3. Make slug required
    op.alter_column(
        "posts",
        "slug",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    # 4. Make slug unique
    op.create_unique_constraint(
        "uq_posts_slug",
        "posts",
        ["slug"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_posts_slug",
        "posts",
        type_="unique",
    )

    op.drop_column("posts", "slug")
