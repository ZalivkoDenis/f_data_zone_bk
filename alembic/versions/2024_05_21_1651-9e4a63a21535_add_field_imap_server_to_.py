"""Add field imap_server to emailSvcProfiles table

Revision ID: 9e4a63a21535
Revises: 046efa9cef42
Create Date: 2024-05-21 16:51:11.191587

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e4a63a21535"
down_revision: Union[str, None] = "046efa9cef42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "email_svc_profiles",
        sa.Column("imap_server", sa.String(length=64), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("email_svc_profiles", "imap_server")
    # ### end Alembic commands ###
