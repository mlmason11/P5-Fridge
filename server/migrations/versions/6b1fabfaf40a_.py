"""empty message

Revision ID: 6b1fabfaf40a
Revises: f53b76463c8b
Create Date: 2023-10-18 01:16:30.873971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b1fabfaf40a'
down_revision = 'f53b76463c8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('saved_recipes', schema=None) as batch_op:
        batch_op.drop_column('is_currently_saved')
        batch_op.drop_column('comment')
        batch_op.drop_column('user_has_made')
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('saved_recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('user_has_made', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('comment', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('is_currently_saved', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###