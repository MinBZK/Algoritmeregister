import pandas as pd
import numpy as np
import json
from pydantic import ValidationError
from app.database.database import SessionLocal
from app import models, schemas
from app.util.logger import get_logger
from app.config.settings import Settings

logger = get_logger(__name__)
env_settings = Settings()


class AlgoritmeLoader:
    """Load algoritmes from a json file. Existing algoritmes will be removed."""

    def __init__(self, json_file: str | None = None):
        if json_file is not None:
            df = self.__get_df_algoritme_from_json(json_file=json_file)
        else:
            raise RuntimeError("Either excel_file or json_file must be specified")

        self.__algoritmes = self.process_df(df)

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
            # Query the AlgoritmeVersion table, which is only populated at the end of
            logging_algos = db.query(models.AlgoritmeVersion).all()
            if (len(logging_algos) == 0) and (env_settings.type != "DEV"):
                logger.info(
                    "No algorithms in database. It is assumed another pod is running the ETL. Stopping loading."
                )
                return False
            db.query(models.Algoritme).delete()
            db.commit()
            for algo in self.__algoritmes:
                lars = algo["lars"]

                algoritme_version_dict = algo.copy()
                algoritme_version_dict.pop("lars")
                algoritme_version_dict.pop("owner")
                new_algoritme_version = models.AlgoritmeVersion(
                    **algoritme_version_dict
                )

                # Makes a new algorithm.
                algoritme_dict = {
                    "lars": lars,
                    "owner": algo["owner"],
                    "versions": [new_algoritme_version],
                }
                new_algoritme = models.Algoritme(**algoritme_dict)

                db.add(new_algoritme)
                db.add(new_algoritme_version)
                logger.info(
                    "Added " + str(lars) + " | " + str(new_algoritme_version.name)
                )

                # Tests validity.
                version_str = "v" + algo["standard_version"].replace(".", "_")
                schema = schemas.versions.create_algorithm_in_loader_schema(version_str)
                try:
                    schema.parse_obj(algo)
                except ValidationError as e:
                    logger.warning(e)
                    counter += len(e.args[0])
            db.commit()
        logger.info("Number of validation errors: " + str(counter))
        return True
