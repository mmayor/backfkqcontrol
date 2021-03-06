"""empty message

Revision ID: 1e4001b4ccb9
Revises: 506264c08dd5
Create Date: 2020-01-09 00:52:11.067512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e4001b4ccb9'
down_revision = '506264c08dd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'test', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test', type_='foreignkey')
    op.drop_column('test', 'user_id')
    # ### end Alembic commands ###
