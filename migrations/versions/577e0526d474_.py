"""empty message

Revision ID: 577e0526d474
Revises: 1acc3d32f03e
Create Date: 2019-01-27 17:18:23.344957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '577e0526d474'
down_revision = '1acc3d32f03e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
