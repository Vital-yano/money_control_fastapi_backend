"""change PHONE_NUMBER length from 11 to 12

Revision ID: 8613508be10e
Revises: 891eaa1788a0
Create Date: 2023-11-18 06:40:18.645771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8613508be10e'
down_revision: Union[str, None] = '891eaa1788a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
