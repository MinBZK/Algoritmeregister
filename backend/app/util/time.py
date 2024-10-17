from app.util.logger import get_logger

import time

time_list: list[int] = [0] * 1000

logger = get_logger("profiler")


def init_time(id: int = 0):
    "Logs start time with reference ID"
    globals()["time_list"][id] = time.time()


def log_time_since(id: int = 0, pre: str | None = None):
    "Prints time since zero time based on reference ID. Resets start time"
    logger.info(
        f"{round((time.time() - globals()['time_list'][id]) * 1000, 3):>7} ms | {pre}"
    )
    init_time(id)


if __name__ == "__main__":
    init_time(999)
    time.sleep(1)
    log_time_since(999)
