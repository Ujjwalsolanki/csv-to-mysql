import os

# Get the base directory of the project (where main.py is located)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# MySQL Connection Configuration
# IMPORTANT: Replace these with your actual MySQL connection details
MYSQL_CONFIG = {
    'host': 'localhost',  # e.g., 'localhost' or '
    'database': 'ETL_WORKFLOW_PROJECT', # e.g., 'my_new_app_db'
    'user': 'root',                   # Your MySQL username
    'password': ''                    # Your MySQL password (empty if no password)
}

# Define the table for data operations
STUDENTS_TABLE = 'students_performance' # Make sure this table exists in your database

# Folder paths for CSV processing
# These paths are relative to the project's base directory
DROPBOX_FOLDER = os.path.join(BASE_DIR, 'dropbox')
ARCHIVE_FOLDER = os.path.join(BASE_DIR, 'archive')

# Logging Configuration
LOGGING_CONFIG = {
    'log_file': os.path.join(BASE_DIR, 'app.log'),
    'log_level': 'INFO' # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
}

# Folder scanning interval in seconds
# For 2 minutes, set to 120. For 30 minutes, set to 1800.
SCAN_INTERVAL_SECONDS = 30 # Default to 2 minutes

# You can add other application-wide settings here if needed
APP_NAME = "MySQL Data Processor"
DEBUG_MODE = True

