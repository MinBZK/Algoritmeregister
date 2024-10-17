import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

LOADING_ENV = os.getenv("LOADING_ENV", "remote")


class Extractor:
    def get_json(self):
        if LOADING_ENV == "local":
            # load from local DB
            with open("app/data.json", "r") as file:
                return json.load(file)

        response = requests.get(
            "https://algoritmes.overheid.nl/api/downloads/site-data/json"
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError("Fetching data failed")


if __name__ == "__main__":
    data = Extractor().get_json()
