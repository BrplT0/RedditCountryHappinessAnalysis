from datetime import datetime
import logging
import sys
from pathlib import Path
import multiprocessing  # Eklendi

_logger_initialized = False  # Eklendi: Global bayrak


def setup_logger(log_dir="data/logs", file_level=logging.DEBUG, console_level=logging.INFO):
    """
    Sets up the logger with separate formatting for file and console.
    Ensures handlers are configured only once, even with multiprocessing.
    """
    global _logger_initialized

    logger = logging.getLogger("reddit_logger")
    logger.setLevel(logging.DEBUG)

    if multiprocessing.current_process().name == 'MainProcess' and not _logger_initialized:

        try:
            log_path_dir = Path(log_dir)
            log_path_dir.mkdir(parents=True, exist_ok=True)

            today_str = datetime.today().strftime("%Y-%m-%d")
            log_file = log_path_dir / f"log_{today_str}.txt"

            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(processName)-12s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_formatter = logging.Formatter('%(levelname)s: %(message)s')

            try:
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(file_formatter)
                file_handler.setLevel(file_level)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"ERROR - MainProcess - Failed to set up file logger at {log_file}: {e}", file=sys.stderr)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(console_level)
            logger.addHandler(console_handler)

            logger.propagate = False

            _logger_initialized = True

            logger.info(
                f"Logging configured. File: {log_file} (Level: {logging.getLevelName(file_level)}), Console Level: {logging.getLevelName(console_level)}")

        except Exception as e:
            print(f"CRITICAL - MainProcess - Failed to configure logging: {e}", file=sys.stderr)

    return logger


if __name__ == "__main__":
    print("Testing logger setup...")
    logger = setup_logger(console_level=logging.DEBUG)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    print("Check the console output and the log file in data/logs.")