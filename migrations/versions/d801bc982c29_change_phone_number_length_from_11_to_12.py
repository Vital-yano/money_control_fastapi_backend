"""change PHONE_NUMBER length from 11 to 12

Revision ID: d801bc982c29
Revises: 3b6662533db8
Create Date: 2023-11-18 07:08:15.827843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd801bc982c29'
down_revision: Union[str, None] = '3b6662533db8'
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
