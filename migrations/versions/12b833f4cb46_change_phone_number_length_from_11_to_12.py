"""change PHONE_NUMBER length from 11 to 12

Revision ID: 12b833f4cb46
Revises: 58016a213d1d
Create Date: 2023-11-18 07:45:48.092735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12b833f4cb46'
down_revision: Union[str, None] = '58016a213d1d'
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
