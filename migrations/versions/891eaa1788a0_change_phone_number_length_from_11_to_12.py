"""change PHONE_NUMBER length from 11 to 12

Revision ID: 891eaa1788a0
Revises: 96c282e881eb
Create Date: 2023-11-16 22:35:36.159663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '891eaa1788a0'
down_revision: Union[str, None] = '96c282e881eb'
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
