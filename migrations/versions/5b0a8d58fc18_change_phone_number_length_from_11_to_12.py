"""change PHONE_NUMBER length from 11 to 12

Revision ID: 5b0a8d58fc18
Revises: 9417e17b751a
Create Date: 2023-12-24 19:23:15.292768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b0a8d58fc18'
down_revision: Union[str, None] = '9417e17b751a'
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
