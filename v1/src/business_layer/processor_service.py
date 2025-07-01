# business_layer/processor_service.py

import os
import shutil
import logging

# Import configurations
from v1.src.config.settings import MYSQL_CONFIG, DROPBOX_FOLDER, ARCHIVE_FOLDER

# Import data layer functions
from v1.src.data_layer.data_reader import read_records
from v1.src.data_layer.csv_processor import process_csv_and_insert_into_mysql

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

def process_all_csv_files(table_name):
    """
    Processes all CSV files found in the dropbox folder, inserts data into MySQL,
    and moves processed files to the archive.
    """
    if not ensure_directories_exist():
        logger.error("Cannot proceed with CSV processing due to directory creation failure.")
        return

    logger.info(f"Checking for new CSV files in '{DROPBOX_FOLDER}'...")
    processed_count = 0
    for filename in os.listdir(DROPBOX_FOLDER):
        if filename.endswith('.csv'):
            file_path = os.path.join(DROPBOX_FOLDER, filename)
            archive_file_path = os.path.join(ARCHIVE_FOLDER, filename)

            logger.info(f"Found CSV file: {filename}. Attempting to process...")
            try:
                # Process the CSV and insert into MySQL
                if process_csv_and_insert_into_mysql(file_path, MYSQL_CONFIG, table_name):
                    # If successful, move the file to the archive folder
                    shutil.move(file_path, archive_file_path)
                    logger.info(f"Successfully processed and moved '{filename}' to '{ARCHIVE_FOLDER}'.")
                    processed_count += 1
                else:
                    logger.error(f"Failed to process '{filename}'. It will remain in the dropbox folder.")
            except Exception as e:
                logger.critical(f"Critical error processing file '{filename}': {e}", exc_info=True)
                # File remains in inbox if a critical error occurs

    if processed_count == 0:
        logger.info("No new CSV files found or processed in the dropbox folder.")
    else:
        logger.info(f"Finished processing {processed_count} CSV files.")

def display_current_database_records(table_name):
    """
    Reads and displays all current records from the specified MySQL table.
    """
    logger.info(f"Reading current records from '{table_name}' table for verification:")
    current_records = read_records(MYSQL_CONFIG, table_name)

    if current_records:
        logger.info(f"Total {len(current_records)} records found in '{table_name}'.")
        # The read_records function (in data_layer/read_data.py) already prints
        # the records to the console. If you wanted to process them further
        # without read_records printing, you'd iterate here.
    else:
        logger.warning(f"No records found in '{table_name}'.")

