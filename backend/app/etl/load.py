from app.etl.resources.loader import AlgoritmeLoader


def load():
    json_file = "app/etl/data/algoritmes_081222.json"
    loader = AlgoritmeLoader(json_file=json_file)
    return loader.load_algoritmes()
