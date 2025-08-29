import logging


def get_logger(name: str):
    # initialize new independent logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
