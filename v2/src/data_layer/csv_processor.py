# data_layer/csv_processor.py

import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_db_connection(mysql_config):
    """
    Establishes and returns a MySQL database connection.
    This is duplicated from read_data.py for self-containment, but in a larger
    application, a single utility function for connection would be better.

    Args:
        mysql_config (dict): A dictionary containing MySQL connection parameters.

    Returns:
        mysql.connector.connection.MySQLConnection or None: The connection object if successful, else None.
    """
    try:
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            database=mysql_config['database'],
            user=mysql_config['user'],
            password=mysql_config['password']
        )
        if connection.is_connected():
            logger.info(f"Successfully connected to MySQL Server version {connection.get_server_info()}")
            return connection
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
    return None

def process_csv_and_insert_into_mysql(file_path, mysql_config, table_name):
    """
    Reads data from a CSV file using pandas and inserts it into a specified MySQL table.

    Args:
        file_path (str): The full path to the CSV file.
        mysql_config (dict): A dictionary containing MySQL connection parameters.
        table_name (str): The name of the table to insert data into.

    Returns:
        bool: True if data was successfully inserted, False otherwise.
    """
    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        logger.info(f"Successfully read CSV file: {file_path}. Rows: {len(df)}")

        if df.empty:
            logger.warning(f"CSV file '{file_path}' is empty. No data to insert.")
            return True # Consider it successful if no data to insert

        connection = get_db_connection(mysql_config)
        if connection is None:
            return False

        cursor = connection.cursor()
        success = False
        try:
            # Prepare the INSERT statement
            # Assuming CSV column names match database column names exactly
            # Exclude 'id' column as it's AUTO_INCREMENT
            columns = [col for col in df.columns if col != 'id']
            placeholders = ', '.join(['%s'] * len(columns))
            column_names_sql = ', '.join(columns)
            insert_query = f"INSERT INTO {table_name} ({column_names_sql}) VALUES ({placeholders})"

            # Convert DataFrame rows to a list of tuples for executemany
            data_to_insert = [tuple(row) for row in df[columns].values]

            # Execute the insert query for all rows
            cursor.executemany(insert_query, data_to_insert)
            connection.commit() # Commit the transaction
            logger.info(f"Successfully inserted {cursor.rowcount} records from '{file_path}' into '{table_name}'.")
            success = True

        except Error as e:
            connection.rollback() # Rollback on error
            logger.error(f"Error inserting data from '{file_path}' into '{table_name}': {e}")
        finally:
            if cursor:
                cursor.close()
                logger.debug("MySQL cursor closed.")
            if connection and connection.is_connected():
                connection.close()
                logger.debug("MySQL connection closed.")
        return success

    except FileNotFoundError:
        logger.error(f"CSV file not found: {file_path}")
        return False
    except pd.errors.EmptyDataError:
        logger.warning(f"CSV file '{file_path}' is empty. No data to process.")
        return True
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV file '{file_path}': {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing CSV '{file_path}': {e}")
        return False

