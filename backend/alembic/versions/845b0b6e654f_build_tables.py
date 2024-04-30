"""build tables

Revision ID: 845b0b6e654f
Revises:
Create Date: 2023-03-07 16:56:50.020821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "845b0b6e654f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "algoritme",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lars", sa.String(length=8), nullable=True),
        sa.Column("leverancier_id", sa.String(length=1024), nullable=True),
        sa.Column("owner", sa.String(length=1024), nullable=True),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_algoritme_id"), "algoritme", ["id"], unique=False)
    op.create_index(op.f("ix_algoritme_lars"), "algoritme", ["lars"], unique=False)

    op.create_table(
        "algoritme_version",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("algoritme_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("organization", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("department", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("description_short", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("type", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("category", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("website", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("status", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("goal", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("impact", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("proportionality", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("decision_making_process", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("documentation", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("competent_authority", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("lawful_basis", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("iama", sa.VARCHAR(length=128), nullable=True),
        sa.Column("iama_description", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("dpia", sa.VARCHAR(length=128), nullable=True),
        sa.Column("dpia_description", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("objection_procedure", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("schema", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("uuid", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("url", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("contact_email", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("area", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("lang", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("revision_date", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("description", sa.VARCHAR(length=10000), nullable=True),
        sa.Column("application_url", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("publiccode", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("mprd", sa.VARCHAR(length=500), nullable=True),
        sa.Column("source_data", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("methods_and_models", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("monitoring", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("human_intervention", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("risks", sa.VARCHAR(length=5000), nullable=True),
        sa.Column("performance_standard", sa.VARCHAR(length=5000), nullable=True),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("end_dt", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "published",
            sa.Boolean,
            nullable=False,
            server_default="False",
        ),
        sa.Column("preview_active", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("created_by", sa.VARCHAR(length=100), nullable=False),
        sa.ForeignKeyConstraint(
            ["algoritme_id"],
            ["algoritme.id"],
            name="algoritme_version_algoritme_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_algoritme_version_id"), "algoritme_version", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_algoritme_version_id"), table_name="algoritme_version")
    op.drop_table("algoritme_version")
    op.drop_index(op.f("ix_algoritme_id"), table_name="algoritme")
    op.drop_index(op.f("ix_algoritme_lars"), table_name="algoritme")
    op.drop_table("algoritme")
