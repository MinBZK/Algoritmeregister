from app.etl.resources.loader import AlgoritmeLoader


def load():
    excel_file = "app/etl/data/2022_12_16_Masterlijst_Algoritmeregister.xlsx"
    loader = AlgoritmeLoader(excel_file=excel_file)
    return loader.load_algoritmes()
