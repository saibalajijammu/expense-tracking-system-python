import logging
import os

def setup_logger(name, log_file='server.log', level=logging.DEBUG):
    # Get absolute path to the log file (so it's always found)
    log_path = os.path.join(os.path.dirname(__file__), log_file)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if already added
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
