"""self-hosted-embedding

Revision ID: 901dc83e8cc1
Revises: 33b0feaf1896
Create Date: 2024-10-10 14:41:16.525309

"""
from alembic import op
import sqlalchemy as sa
from app.embeddors.bert import Embeddor
from sqlalchemy.sql import text
from app.util.logger import get_logger

logger = get_logger(__name__)

# revision identifiers, used by Alembic.
revision = "901dc83e8cc1"
down_revision = "33b0feaf1896"
branch_labels = None
depends_on = None


def _embed_db(embeddor, column_name):
    logger.info("Add embedding table")
    op.execute(
        f"""
        ALTER TABLE algoritme_version
        ADD COLUMN {column_name} vector({int(embeddor.modelsize)});
        """
    )
    logger.info("Create index")
    op.execute(
        f"CREATE INDEX IF NOT EXISTS algoritme_version_{column_name}_idx ON algoritme_version USING hnsw ({column_name} vector_l2_ops);"
    )
    logger.info("Create function for trigger")
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION set_placeholder_embedding()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.{column_name} = array_fill(0.0, ARRAY[{embeddor.modelsize}]);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    logger.info("Create trigger")
    op.execute(
        f"""
        CREATE TRIGGER trigger_set_placeholder_embedding
        BEFORE INSERT ON algoritme_version
        FOR EACH ROW
        EXECUTE FUNCTION set_placeholder_embedding();
        """
    )
    logger.info("Update column with placeholder value")
    placeholder_vector = "[" + ", ".join(map(str, [0.0] * embeddor.modelsize)) + "]"
    op.execute(
        f"""
        UPDATE algoritme_version
        SET {column_name} = '{placeholder_vector}';
        """
    )


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    _embed_db(
        Embeddor(
            "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers"
        ),
        "embedding_nfi",
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_set_placeholder_embedding ON algoritme_version;")
    op.execute("DROP FUNCTION IF EXISTS set_placeholder_embedding;")
    op.execute("ALTER TABLE algoritme_version DROP COLUMN embedding_nfi;")
