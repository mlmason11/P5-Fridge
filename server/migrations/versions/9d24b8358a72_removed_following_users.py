"""Removed following users

Revision ID: 9d24b8358a72
Revises: 63fafdc91d0c
Create Date: 2023-10-17 16:22:24.952614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d24b8358a72'
down_revision = '63fafdc91d0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_follows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_follows',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('follower_id', sa.INTEGER(), nullable=True),
    sa.Column('followee_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['followee_id'], ['users.id'], name='fk_user_follows_followee_id_users'),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], name='fk_user_follows_follower_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
