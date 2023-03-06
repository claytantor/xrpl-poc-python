"""set shop data

Revision ID: b0b0233542b2
Revises: deafb9cf44c2
Create Date: 2023-03-03 10:31:30.554779

"""
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b0233542b2'
down_revision = 'deafb9cf44c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # shop_id = op.get_bind().execute("SELECT id FROM shop LIMIT 1").fetchone()[0]
    # iterate over all wallets
    for wallet in op.get_bind().execute("SELECT id, shop_id, shop_name, classic_address FROM wallet"):
        # update the shop id and name
        shop_id = str(uuid.uuid4()).replace('-', '')[:10]
        op.get_bind().execute('UPDATE wallet SET shop_id = %s, shop_name = %s WHERE id = %s', (shop_id, wallet[3], wallet[0]))


def downgrade() -> None:
    for wallet in op.get_bind().execute("SELECT id, shop_id, shop_name, classic_address FROM wallet"):
        # update the shop id and name
        op.get_bind().execute('UPDATE wallet SET shop_id = %s, shop_name = %s WHERE id = %s', (None, None, wallet[0]))
