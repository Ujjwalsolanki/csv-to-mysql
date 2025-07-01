# utils/logger.py

import logging
import os

def setup_logging(log_file_path, log_level_str='INFO'):
    """
    Configures the logging for the application.

    Args:
        log_file_path (str): The full path to the log file.
        log_level_str (str): The desired logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    """
    numeric_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler() # Also log to console
        ]
    )
    # Return the root logger instance
    return logging.getLogger()