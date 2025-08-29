"""add_ROO_columns_to_organisation

Revision ID: 0c2d4ffb07ff
Revises: 901dc83e8cc1
Create Date: 2025-03-07 15:08:11.267885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c2d4ffb07ff'
down_revision = '901dc83e8cc1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("organisation", sa.Column("org_id", sa.VARCHAR(), nullable=True, unique=True))
    op.add_column("organisation", sa.Column("official_name", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("alternative_name", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("abbreviation", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("roo_type", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("part_of", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("relation_with_ministry", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("tooi_uri", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("kvk_number", sa.Integer(), nullable=True))
    op.add_column("organisation", sa.Column("organisation_code", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("tooi_uri_regional_collaboration_body", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("label", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("official_name_with_type", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("official_name_without_type", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("official_name_for_sorting", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("preferred_name_without_type", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("preferred_name_including_type", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("preferred_name_for_sorting", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("tooi_alternative_name", sa.VARCHAR(), nullable=True))
    op.add_column("organisation", sa.Column("last_updated_dt_tooi", sa.TIMESTAMP(timezone=True), server_default=None, nullable=True))
    op.create_unique_constraint("uq_organisation_code", "organisation", ["code"])

def downgrade() -> None:
    op.drop_column("organisation", "org_id")
    op.drop_column("organisation", "official_name")
    op.drop_column("organisation", "alternative_name")
    op.drop_column("organisation", "abbreviation")
    op.drop_column("organisation", "roo_type")
    op.drop_column("organisation", "part_of")
    op.drop_column("organisation", "relation_with_ministry")
    op.drop_column("organisation", "tooi_uri")
    op.drop_column("organisation", "kvk_number")
    op.drop_column("organisation", "organisation_code")
    op.drop_column("organisation", "tooi_uri_regional_collaboration_body")
    op.drop_column("organisation", "label")
    op.drop_column("organisation", "official_name_with_type")
    op.drop_column("organisation", "official_name_without_type")
    op.drop_column("organisation", "official_name_for_sorting")
    op.drop_column("organisation", "preferred_name_without_type")
    op.drop_column("organisation", "preferred_name_including_type")
    op.drop_column("organisation", "preferred_name_for_sorting")
    op.drop_column("organisation", "tooi_alternative_name")
    op.drop_column("organisation", "last_updated_dt_tooi")
    op.drop_constraint("uq_organisation_code", "organisation", type_="unique")
