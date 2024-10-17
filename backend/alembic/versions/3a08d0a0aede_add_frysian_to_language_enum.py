"""Add frysian to language enum

Revision ID: 3a08d0a0aede
Revises: a3ff62ca5a84
Create Date: 2024-03-28 11:35:36.416446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a08d0a0aede"
down_revision = "243d3a6d2320"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Temporary enum trick to safely alter the enum in postgres
    new_enum = sa.Enum("NLD", "ENG", "FRY", name="_tmp_enum")
    new_enum.create(op.get_bind(), checkfirst=False)

    # Alter the 'language' columns in 'algoritme_version' and 'organisation_details' to use the tmp ENUM type
    op.execute(
        "ALTER TABLE algoritme_version ALTER COLUMN language TYPE _tmp_enum USING language::text::_tmp_enum"
    )
    op.execute(
        "ALTER TABLE organisation_details ALTER COLUMN language TYPE _tmp_enum USING language::text::_tmp_enum"
    )

    # Drop the old ENUM type if it's not used anywhere else
    op.execute("DROP TYPE language")

    # Rename the tmp ENUM type back to 'language'
    op.execute("ALTER TYPE _tmp_enum RENAME TO language")


def downgrade() -> None:
    # Temporary enum trick to safely alter the enum in postgres
    new_enum = sa.Enum("NLD", "ENG", name="_tmp_enum")
    new_enum.create(op.get_bind(), checkfirst=False)

    # Alter the 'language' columns in 'algoritme_version' and 'organisation_details' to use the tmp ENUM type
    op.execute(
        "ALTER TABLE algoritme_version ALTER COLUMN language TYPE _tmp_enum USING language::text::_tmp_enum"
    )
    op.execute(
        "ALTER TABLE organisation_details ALTER COLUMN language TYPE _tmp_enum USING language::text::_tmp_enum"
    )

    # Drop the old ENUM type if it's not used anywhere else
    op.execute("DROP TYPE language")

    # Rename the tmp ENUM type back to 'language'
    op.execute("ALTER TYPE _tmp_enum RENAME TO language")
