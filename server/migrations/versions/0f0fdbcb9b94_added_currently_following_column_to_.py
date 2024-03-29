"""added currently_following column to UserFollow

Revision ID: 0f0fdbcb9b94
Revises: 48691b07e9b9
Create Date: 2023-10-13 15:02:10.491632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f0fdbcb9b94'
down_revision = '48691b07e9b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('saved_recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_has_made', sa.Boolean(), nullable=True))

    with op.batch_alter_table('user_follows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currently_following', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_follows', schema=None) as batch_op:
        batch_op.drop_column('currently_following')

    with op.batch_alter_table('saved_recipes', schema=None) as batch_op:
        batch_op.drop_column('user_has_made')

    # ### end Alembic commands ###
