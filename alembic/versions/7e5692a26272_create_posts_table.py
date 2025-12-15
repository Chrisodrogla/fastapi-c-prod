"""create posts table

Revision ID: 7e5692a26272
Revises: 
Create Date: 2025-12-15 18:55:46.311319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e5692a26272'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table ('users', sa. Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('email', sa.String, unique=True, index=True, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))    )

    """Upgrade schema."""
  
    pass


def downgrade() -> None:
    op.drop_table('users')
    """Downgrade schema."""
    pass





# def upgrade() -> None:
#     op.create_table(
#         'posts',
#         sa.Column('id', sa.Integer, primary_key=True, index=True),
#         sa.Column('title', sa.String, nullable=False),
#         sa.Column('content', sa.String, nullable=False),
#         sa.Column('published', sa.Boolean, server_default='True', nullable=False),
#         sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
#         sa.Column('rating', sa.Integer, nullable=False),
#         sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete= "CASCADE")),
#     )
#     """Upgrade schema."""
#     pass


# def downgrade() -> None:
#     op.drop_table('posts')
#     """Downgrade schema."""
#     pass
