from datetime import datetime
import logging
import sys
from pathlib import Path


def setup_logger():
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent

    log_dir = project_root / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.today().strftime("%Y-%m-%d")
    log_filename = log_dir / f"log_{today_str}.txt"

    logger = logging.getLogger("reddit_logger")

    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"📋 Log file: data\\logs\\log_{today_str}.txt")

    return logger


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Logger is working ✅")
