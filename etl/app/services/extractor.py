import requests


class Extractor:
    def get_json(self):
        response = requests.get("https://algoritmes.overheid.nl/api/json/algoritme")
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError("Fetching data failed")


if __name__ == "__main__":
    json = Extractor().get_json()
