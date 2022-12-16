import pandas as pd
import numpy as np
import json
from app.database.database import SessionLocal
from app.etl.config.main import models, column_grouping
from app.etl.config.excel_column_mapping import excel_column_mapping
from slugify import slugify


class AlgoritmeLoader:
    """Load algoritmes from a json file. Existing algoritmes will be removed."""

    def __init__(self, excel_file: str | None = None, json_file: str | None = None):

        if excel_file is not None:
            df = self.__get_df_algoritme_from_excel(excel_file)
        elif json_file is not None:
            df = self.__get_df_algoritme_from_json(json_file=json_file)
        else:
            raise RuntimeError("Either excel_file or json_file must be specified")

        self.__algoritmes = self.process_df(df)

    @staticmethod
    def __get_df_algoritme_from_excel(excel_file: str) -> pd.DataFrame:
        sheet_names = pd.read_excel(excel_file, sheet_name=None).keys()
        included_sheet_names = [
            sheet_name
            for sheet_name in sheet_names
            if sheet_name not in ["Template (dupliceer dit blad)", "Lege invullijst"]
        ]
        sheet_name = included_sheet_names[0]
        df_all = pd.DataFrame()
        for sheet_name in included_sheet_names:
            df = (
                pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                .drop(columns=[0])
                .set_index(1)
                .T
            )
            df_all = pd.concat([df_all, df])
        return df_all.rename(columns=excel_column_mapping)

    @staticmethod
    def __get_df_algoritme_from_json(json_file: str) -> pd.DataFrame:
        with open(json_file) as f:
            algoritmes: list[dict] = json.load(f)
        df = pd.DataFrame(algoritmes)[3:]
        return df

    @staticmethod
    def process_df(df: pd.DataFrame) -> list[dict]:
        df.columns = df.columns.str.lower()

        boolean_cols = ["dpia", "mprd"]
        non_null_columns = [c for c in list(df.columns) if c not in boolean_cols]

        string_cols = [
            "source_data",
        ]

        for bc in boolean_cols:
            df[bc] = df[bc].map({"Ja": True, "Nee": False, np.nan: None})

        for nc in non_null_columns:
            df[nc] = df[nc].fillna("")

        for sc in string_cols:
            df[sc] = df[sc].str.slice(0, 5000)

        return df.replace({np.nan: None}).to_dict(orient="records")

    def __get_model_from_algoritme_data(self, algoritme: dict, model_key: str):
        kwargs = {c: algoritme[c] for c in column_grouping[model_key]}
        model = models[model_key](**kwargs)
        return model

    def load_algoritmes(self):

        algoritmes = self.__algoritmes

        with SessionLocal() as session:
            session.query(models["algoritme"]).delete()
            session.commit()

            # insert algoritmes
            for a in algoritmes:
                new_algoritme = self.__get_model_from_algoritme_data(
                    algoritme=a, model_key="algoritme"
                )
                a_name: str = new_algoritme.name
                a_organization: str = new_algoritme.organization
                new_algoritme.slug = self.slugify_str_list([a_name, a_organization])

                property_keys = [key for key in models.keys() if key != "algoritme"]
                for pk in property_keys:
                    setattr(
                        new_algoritme,
                        pk,
                        self.__get_model_from_algoritme_data(algoritme=a, model_key=pk),
                    )

                session.add(new_algoritme)

            session.commit()
            return True

    @staticmethod
    def slugify_str_list(str_list: list[str]):
        return slugify("-".join(str_list))
