import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent / "data/logs"
LOG_DIR.mkdir(exist_ok=True)


def getLogger(name, filename):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fileHandler = logging.FileHandler(LOG_DIR / filename, encoding="utf-8")
    fileHandler.setFormatter(formatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger
