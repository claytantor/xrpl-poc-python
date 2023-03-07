"""customer account

Revision ID: a66d29695fb0
Revises: b0b0233542b2
Create Date: 2023-03-06 14:48:28.242388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66d29695fb0'
down_revision = 'b0b0233542b2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_account', sa.Column('account_wallet_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'customer_account', 'wallet', ['account_wallet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'customer_account', type_='foreignkey')
    op.drop_column('customer_account', 'account_wallet_id')
    # ### end Alembic commands ###
