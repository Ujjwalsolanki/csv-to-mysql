import time # Import the time module for sleep functionality

### Version 3.0.0 configurations
# Import configurations
from v3.src.config.settings import LOGGING_CONFIG, SCAN_INTERVAL_SECONDS, DROPBOX_FOLDER, STUDENTS_TABLE
# Import logging setup from utilities
from v3.src.data_layer.csv_handler import CSVHandler
from v3.src.utils.logger import setup_logging
# Import functions from the business layer
from v3.src.business_layer.processor_service import process_all_csv_files, display_current_database_records, ensure_directories_exist
import time
from watchdog.observers import Observer

def main():
    """
    Main function to run the MySQL data processing application.
    Orchestrates the application flow using watchdog for real-time file monitoring.
    """
    # Setup logging for the entire application
    logger = setup_logging(
        log_file_path=LOGGING_CONFIG['log_file'],
        log_level_str=LOGGING_CONFIG['log_level']
    )
    logger.info("Starting MySQL Data Processor Application...")

    # Ensure directories exist at startup
    ensure_directories_exist()

    # Perform an initial scan for any CSV files already present in the folder
    logger.info("Performing initial scan for existing CSV files...")
    process_all_csv_files(STUDENTS_TABLE)

    # Display current records in the database after initial scan
    display_current_database_records(STUDENTS_TABLE)

    logger.info(f"Starting watchdog to monitor '{DROPBOX_FOLDER}' for new CSV files...")
    logger.info("Press Ctrl+C to stop the application.")

    # Setup watchdog observer
    event_handler = CSVHandler(STUDENTS_TABLE)
    observer = Observer()
    observer.schedule(event_handler, DROPBOX_FOLDER, recursive=False) # Only watch the top-level folder

    try:
        observer.start() # Start the observer thread
        while True:
            time.sleep(1) # Keep the main thread alive
    except KeyboardInterrupt:
        logger.info("Application stopped by user (Ctrl+C).")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
    finally:
        observer.stop() # Stop the observer thread
        observer.join() # Wait until the observer thread terminates
        logger.info("Application finished.")

if __name__ == "__main__":
    main()
