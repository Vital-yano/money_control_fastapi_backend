"""change PHONE_NUMBER length from 11 to 12

Revision ID: 1cc26f1f82d2
Revises: 0129241e37bf
Create Date: 2023-12-24 16:59:03.820648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cc26f1f82d2'
down_revision: Union[str, None] = '0129241e37bf'
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
