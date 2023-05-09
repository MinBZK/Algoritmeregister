import pandas as pd
import numpy as np
import json
from pydantic import ValidationError
from app.database.database import SessionLocal
from app.etl.config.excel_column_mapping import excel_column_mapping
from app import models, schemas
from app.util import upc


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

        df_all["lars"] = None
        df_all["published"] = True
        df_all["released"] = True
        df_all["Schema"] = "0.1.0"
        df_all["Herzieningsdatum"] = df_all["Herzieningsdatum"].astype("string")

        return df_all.rename(columns=excel_column_mapping)

    @staticmethod
    def __get_df_algoritme_from_json(json_file: str) -> pd.DataFrame:
        with open(json_file) as f:
            algoritmes: list[dict] = json.load(f)
        df = pd.DataFrame(algoritmes)
        return df

    @staticmethod
    def process_df(df: pd.DataFrame) -> list[dict]:
        string_cols = [
            "source_data",
            "description_short",
        ]
        for sc in string_cols:
            df[sc] = df[sc].str.slice(0, 5000)

        # build a column to indicate who owns the algorithm. If there are two parties (separated by a comma), take the
        # first one.
        if "owner" not in df.columns:
            df["owner"] = (
                df.organization.replace(" ", "-", regex=True)
                .apply(str.lower)
                .str.split(pat=",", expand=True)[0]
            )

        df = df.replace(
            {
                "owner": {
                    "ministerie-van-financiën": "ministerie-fin",
                    "ministerie-van-economische-zaken-en-klimaat": "ministerie-ezk",
                    "sociale-verzekeringsbank-(svb)": "sociale-verzekeringsbank",
                    "uitvoeringsinstituut-werknemersverzekeringen-(uwv)": "uitvoeringsinstituut-werknemersver"
                    "zekeringen",
                    "rijksdienst-voor-identiteitsgegevens-(rvig)": "rijksdienst-voor-identiteitsgegevens",
                }
            }
        )

        return df.replace({np.nan: None}).to_dict(orient="records")

    def load_algoritmes(self):
        counter = 0
        with SessionLocal() as db:
            db.query(models.Algoritme).delete()
            db.commit()
            for new_version in self.__algoritmes:
                # Checks presence in db based on LARS-code.
                lars = new_version["lars"]
                if lars:
                    algo_in_db = (
                        db.query(models.Algoritme)
                        .filter(models.Algoritme.lars == lars)
                        .first()
                    )
                else:
                    algo_in_db = None

                if not algo_in_db:
                    # If not found, makes a new algorithm.

                    # Test provided LARS-code for validity.
                    lars_is_valid = upc.validate_upc(new_version["lars"])
                    if not lars_is_valid:
                        # Redefines LARS-code.
                        lars_list = [
                            id[0] for id in db.query(models.Algoritme.id).all()
                        ]
                        lars = upc.find_new_upc(avoid_upc_list=lars_list)

                    # Makes a new algorithm.
                    algoritme_dict = {
                        "lars": lars,
                        "owner": new_version["owner"],
                    }
                    new_algoritme = models.Algoritme(**algoritme_dict)
                    db.add(new_algoritme)
                    db.flush()
                    db.refresh(new_algoritme)
                    algoritme_id = new_algoritme.id
                else:
                    # If found, archive newest algo
                    algoritme_id = algo_in_db.id

                # add a new algorithm_version
                # Remove all the columns that belong in the 'algoritme' table.
                new_version.pop("lars")
                new_version.pop("owner")
                new_version["algoritme_id"] = algoritme_id
                new_version_model = models.AlgoritmeVersion(**new_version)

                # test validity

                version_str = "v" + new_version["standard_version"].replace(".", "_")
                schema = schemas.versions.create_algorithm_in_loader_schema(version_str)
                try:
                    schema.parse_obj(new_version)
                except ValidationError as e:
                    print(e)
                    counter += len(e.args[0])

                db.add(new_version_model)
                db.commit()
        print("Number of validation errors:", counter)
        return True
