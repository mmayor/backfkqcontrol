"""empty message

Revision ID: e0bcf16d53b7
Revises: 4c028bb27264
Create Date: 2020-01-07 03:33:19.810196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0bcf16d53b7'
down_revision = '4c028bb27264'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('dateNew', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'dateNew')
    # ### end Alembic commands ###
