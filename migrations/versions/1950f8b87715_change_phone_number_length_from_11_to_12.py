"""change PHONE_NUMBER length from 11 to 12

Revision ID: 1950f8b87715
Revises: ffc830d1e84a
Create Date: 2023-11-18 07:31:04.904210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1950f8b87715'
down_revision: Union[str, None] = 'ffc830d1e84a'
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
