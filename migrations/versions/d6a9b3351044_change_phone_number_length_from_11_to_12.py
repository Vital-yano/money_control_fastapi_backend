"""change PHONE_NUMBER length from 11 to 12

Revision ID: d6a9b3351044
Revises: 31ca29d230b3
Create Date: 2023-12-24 17:00:52.266913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6a9b3351044'
down_revision: Union[str, None] = '31ca29d230b3'
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
