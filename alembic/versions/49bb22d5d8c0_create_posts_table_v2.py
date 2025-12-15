"""create posts table v2

Revision ID: 49bb22d5d8c0
Revises: 7e5692a26272
Create Date: 2025-12-15 19:08:00.444163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49bb22d5d8c0'
down_revision: Union[str, Sequence[str], None] = '7e5692a26272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='True', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete= "CASCADE")),
    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('posts')
    """Downgrade schema."""
    pass
