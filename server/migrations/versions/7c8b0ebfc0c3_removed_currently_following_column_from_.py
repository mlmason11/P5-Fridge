"""Removed currently_following column from UserFollow

Revision ID: 7c8b0ebfc0c3
Revises: 0f0fdbcb9b94
Create Date: 2023-10-15 18:25:50.161865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8b0ebfc0c3'
down_revision = '0f0fdbcb9b94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_follows', schema=None) as batch_op:
        batch_op.drop_column('currently_following')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_follows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currently_following', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
