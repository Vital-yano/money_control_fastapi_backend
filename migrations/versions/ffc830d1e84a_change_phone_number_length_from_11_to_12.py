"""change PHONE_NUMBER length from 11 to 12

Revision ID: ffc830d1e84a
Revises: edb34e90b2ee
Create Date: 2023-11-18 07:29:46.455534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffc830d1e84a'
down_revision: Union[str, None] = 'edb34e90b2ee'
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
