"""change PHONE_NUMBER length from 11 to 12

Revision ID: 4ac12341e065
Revises: e023065edd84
Create Date: 2023-11-18 07:40:38.646962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ac12341e065'
down_revision: Union[str, None] = 'e023065edd84'
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
