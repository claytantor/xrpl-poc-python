"""add shop wallet

Revision ID: deafb9cf44c2
Revises: ae0c30506def
Create Date: 2023-03-03 10:30:33.256673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deafb9cf44c2'
down_revision = 'ae0c30506def'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wallet', sa.Column('shop_id', sa.String(length=10), nullable=True))
    op.add_column('wallet', sa.Column('shop_name', sa.String(length=100), nullable=True))
    op.add_column('wallet', sa.Column('shop_description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wallet', 'shop_description')
    op.drop_column('wallet', 'shop_name')
    op.drop_column('wallet', 'shop_id')
    # ### end Alembic commands ###