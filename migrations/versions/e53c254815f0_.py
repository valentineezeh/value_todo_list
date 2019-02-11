"""empty message

Revision ID: e53c254815f0
Revises: 577e0526d474
Create Date: 2019-01-31 13:29:29.725926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e53c254815f0'
down_revision = '577e0526d474'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('confirmed_on_date', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('registered_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'registered_on')
    op.drop_column('users', 'confirmed_on_date')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###