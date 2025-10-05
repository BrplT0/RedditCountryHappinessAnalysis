from datetime import datetime
import logging
import sys

def setup_logger():
    today_str = datetime.today().strftime("%Y-%m-%d")
    log_filename = f"../../data/logs/log_{today_str}.txt"

    logger = logging.getLogger("reddit_logger")
    logger.setLevel(logging.INFO)
    logger.handlers = []

    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger