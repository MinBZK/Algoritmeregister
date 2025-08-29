import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

LOADING_ENV = os.getenv("LOADING_ENV", "local")


class Extractor:
    def get_json(self):
        if LOADING_ENV == "local":
            # load from local DB
            with open("app/data.json", "r") as file:
                return json.load(file)

if __name__ == "__main__":
    data = Extractor().get_json()
