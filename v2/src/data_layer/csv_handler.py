import logging
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from v2.src.business_layer.processor_service import process_single_csv_file

class CSVHandler(FileSystemEventHandler):
    """
    Custom event handler for watchdog to process CSV file system events.
    """
    def __init__(self, table_name):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.table_name = table_name

    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory and event.src_path.endswith('.csv'):
            self.logger.info(f"Watchdog detected new CSV file created: {event.src_path}")
            # Add a small delay to ensure the file is fully written
            time.sleep(0.5) # Wait for 500 milliseconds
            process_single_csv_file(event.src_path, self.table_name)

    def on_modified(self, event):
        """Called when a file or directory is modified."""
        # This can sometimes trigger for files being written.
        # We might want to add a small delay or a check to ensure the file is fully written.
        if not event.is_directory and event.src_path.endswith('.csv'):
            self.logger.info(f"Watchdog detected CSV file modified: {event.src_path}")
            # Add a small delay to ensure the file is fully written
            time.sleep(0.5) # Wait for 500 milliseconds
            # Only process if the file still exists and hasn't been moved by a previous event
            if os.path.exists(event.src_path):
                process_single_csv_file(event.src_path, self.table_name)