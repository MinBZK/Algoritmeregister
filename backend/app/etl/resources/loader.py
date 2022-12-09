import pandas as pd
import numpy as np
import json
from app.database.database import SessionLocal
from app.etl.config.main import models, column_grouping
from dataclasses import dataclass
from slugify import slugify


@dataclass
class AlgoritmeLoader:
    """Load algoritmes from a json file. Existing algoritmes will be removed."""

    json_file: str

    @property
    def __algoritmes(self):
        with open(self.json_file) as f:
            algoritmes: list[dict] = json.load(f)
        df = pd.DataFrame(algoritmes)[3:]
        df.columns = df.columns.str.lower()

        boolean_cols = ["dpia", "mprd"]
        # non_null_columns = [c for c in list(df.columns) if c not in boolean_cols]
        string_cols = [
            # "description_short",
            # "description",
            "source_data",
            # "methods_and_models",
        ]

        for bc in boolean_cols:
            df[bc] = df[bc].map({"Ja": True, "Nee": False, np.nan: None})

        # for nc in non_null_columns:
        #     df[nc] = df[nc].fillna("-")

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
