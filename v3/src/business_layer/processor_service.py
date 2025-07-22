import os
import shutil
import logging

# Import configurations
from v2.src.config.settings import MYSQL_CONFIG, DROPBOX_FOLDER, ARCHIVE_FOLDER

# Import data layer functions
from v2.src.data_layer.data_reader import read_records
from v2.src.data_layer.csv_processor import process_csv_and_insert_into_mysql

logger = logging.getLogger(__name__)

def ensure_directories_exist():
    """Ensures that the dropbox and archive directories exist."""
    try:
        os.makedirs(DROPBOX_FOLDER, exist_ok=True)
        os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
        logger.info(f"Ensured '{DROPBOX_FOLDER}' and '{ARCHIVE_FOLDER}' directories exist.")
        return True
    except OSError as e:
        logger.error(f"Error creating directories: {e}")
        return False

def process_single_csv_file(file_path, table_name):
    """
    Processes a single CSV file, inserts data into MySQL, and moves it to the archive.

    Args:
        file_path (str): The full path to the CSV file to process.
        table_name (str): The name of the MySQL table to insert data into.

    Returns:
        bool: True if the file was successfully processed and moved, False otherwise.
    """
    filename = os.path.basename(file_path)
    archive_file_path = os.path.join(ARCHIVE_FOLDER, filename)

    logger.info(f"Attempting to process single CSV file: {filename}...")
    try:
        if process_csv_and_insert_into_mysql(file_path, MYSQL_CONFIG, table_name):
            shutil.move(file_path, archive_file_path)
            logger.info(f"Successfully processed and moved '{filename}' to '{ARCHIVE_FOLDER}'.")
            return True
        else:
            logger.error(f"Failed to process '{filename}'. It will remain in the dropbox folder.")
            return False
    except Exception as e:
        logger.critical(f"Critical error processing single file '{filename}': {e}", exc_info=True)
        return False
    
def csv_file_generator(directory):
    """Yields one CSV file path at a time from the specified directory."""
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.csv'):
                yield entry.path


def process_all_csv_files(table_name):
    """
    Processes CSV files one-by-one from the DROPBOX_FOLDER.
    Useful for an initial scan when the application starts.
    """
    if not ensure_directories_exist():
        logger.error("Cannot proceed with CSV processing due to directory creation failure.")
        return

    logger.info(f"Performing initial scan for CSV files in '{DROPBOX_FOLDER}'...")
    processed_count = 0

    for file_path in csv_file_generator(DROPBOX_FOLDER):
        if process_single_csv_file(file_path, table_name):
            processed_count += 1

    if processed_count == 0:
        logger.info("No existing CSV files found or processed during initial scan.")
    else:
        logger.info(f"Finished initial scan, processed {processed_count} CSV files.")

def display_current_database_records(table_name):
    """
    Reads and displays all current records from the specified MySQL table.
    """
    logger.info(f"Reading current records from '{table_name}' table for verification:")
    current_records = read_records(MYSQL_CONFIG, table_name)

    if current_records:
        logger.info(f"Total {len(current_records)} records found in '{table_name}'.")
        # The read_records function (in data_layer/read_data.py) already prints
        # the records to the console.
    else:
        logger.warning(f"No records found in '{table_name}'.")
