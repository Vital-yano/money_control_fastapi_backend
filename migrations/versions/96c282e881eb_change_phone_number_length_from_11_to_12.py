"""change PHONE_NUMBER length from 11 to 12

Revision ID: 96c282e881eb
Revises: fa0da3b73674
Create Date: 2023-11-16 22:34:17.545270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96c282e881eb'
down_revision: Union[str, None] = 'fa0da3b73674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_account', 'phone_number',
               existing_type=sa.VARCHAR(length=11),
               type_=sa.String(length=12),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_account', 'phone_number',
               existing_type=sa.String(length=12),
               type_=sa.VARCHAR(length=11),
               existing_nullable=False)
    # ### end Alembic commands ###
