"""add post status

Revision ID: 8e50dd073f03
Revises: bf751bbec182
Create Date: 2026-09-12 13:00:38.649293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e50dd073f03'
down_revision: Union[str, Sequence[str], None] = 'bf751bbec182'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=True,
            server_default="draft",
        ),
    )

    op.execute(
        "UPDATE posts SET status = 'published' WHERE status IS NULL"
    )

    op.alter_column(
        "posts",
        "status",
        nullable=False,
        server_default="draft",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "status")
