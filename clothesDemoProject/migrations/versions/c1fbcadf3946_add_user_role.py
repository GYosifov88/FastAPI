"""add user role

Revision ID: c1fbcadf3946
Revises: 1cca2f6b9769
Create Date: 2023-05-26 13:20:02.100439

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c1fbcadf3946'
down_revision = '1cca2f6b9769'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    user_role = postgresql.ENUM('super_admin', 'admin', 'user', name='user_role')
    user_role.create(op.get_bind())
    op.add_column('users', sa.Column('role', sa.Enum('super_admin', 'admin', 'user', name='user_role'), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
