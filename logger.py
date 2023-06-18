import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, mode: str, level=logging.INFO):
    """Name: name of the logger to access, log_file: name of the file itself, mode: string 'a'-append; 'w'-write, format: True adds time, levelname and message, level sets default to INFO. Format as following: '%(asctime)s %(processName)s - %(name)s:%(lineno)d - %(levelname)s %(message)s'"""
    formatter = logging.Formatter(
        "%(asctime)s %(processName)s - %(name)s:%(lineno)d - %(levelname)s %(message)s"
    )

    dir_path = "./logs/"
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(dir_path + log_file + ".log", mode)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger, dir_path
