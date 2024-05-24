"""Add wholesale_price and retail_price to Product.

Revision ID: 4bbe5e494cd1
Revises: 3d52ec9ec439
Create Date: 2024-05-23 10:39:52.795111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bbe5e494cd1'
down_revision = '3d52ec9ec439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wholesale_price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('retail_price', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('retail_price')
        batch_op.drop_column('wholesale_price')

    # ### end Alembic commands ###