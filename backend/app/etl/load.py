from app.etl.resources.loader import AlgoritmeLoader


def load_excel():
    excel_file = "app/etl/data/Masterlijst_Algoritmeregister.xlsx"
    loader = AlgoritmeLoader(excel_file=excel_file)
    return loader.load_algoritmes()


def load_json():
    json_file = "app/etl/data/pub_data.json"
    loader = AlgoritmeLoader(json_file=json_file)
    return loader.load_algoritmes()


if __name__ == "__main__":
    from app.util.logger import get_logger

    logger = get_logger(__name__)

    # data_loaded = load_json()
    data_loaded = load_excel()
    if data_loaded:
        logger.info("Algoritmes loaded")
    else:
        logger.info("Data not loaded")
