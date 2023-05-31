"""postal code

Revision ID: 071e2bbcf793
Revises: 4143c8626f02
Create Date: 2023-05-25 17:34:25.094167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '071e2bbcf793'
down_revision = '4143c8626f02'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('postal_code', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'postal_code')
    # ### end Alembic commands ###