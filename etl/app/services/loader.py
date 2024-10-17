import pandas as pd
from sqlalchemy import text, types
from typing import Literal
from app.report.logger import get_logger
from app.database.config import engine

logger = get_logger(__name__)


class Loader:
    def load(
        self,
        df: pd.DataFrame | None,
        table_name: Literal[
            "algoritme", "algoritme_version", "organisation", "organisation_details"
        ],
        dtypes: dict = {},
    ) -> None:
        if df is None:
            return

        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {table_name};"))
            conn.commit()

        df.to_sql(table_name, engine, if_exists="append", index=False, dtype=dtypes)

        # auto-increment must be reset.
        max_value_sql = f"SELECT MAX(id) FROM {table_name}"
        with engine.connect() as conn:
            max_value = conn.execute(text(max_value_sql)).scalar()
            reset_sequence_sql = f"SELECT setval('{table_name}_id_seq', {max_value})"
            conn.execute(text(reset_sequence_sql))

    def update_database(
        self,
        df_organisation: pd.DataFrame,
        df_organisation_details: pd.DataFrame,
        df_algoritme: pd.DataFrame,
        df_algoritme_version: pd.DataFrame,
    ) -> None:
        self.load(df_organisation, "organisation")
        self.load(df_organisation_details, "organisation_details")
        self.load(df_algoritme, "algoritme")

        json_columns = [
            "lawful_basis_grouping",
            "impacttoetsen_grouping",
            "source_data_grouping",
        ]
        dtypes = {column_name: types.JSON for column_name in json_columns}
        self.load(df_algoritme_version, "algoritme_version", dtypes)
