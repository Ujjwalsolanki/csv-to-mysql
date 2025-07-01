# data_layer/read_data.py

import mysql.connector
from mysql.connector import Error
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_db_connection(mysql_config):
    """
    Establishes and returns a MySQL database connection.

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

def read_records(mysql_config, table_name):
    """
    Connects to a MySQL database using provided configuration and reads all data from a specified table.

    Args:
        mysql_config (dict): A dictionary containing MySQL connection parameters
                             (e.g., 'host', 'database', 'user', 'password').
        table_name (str): The name of the table to read data from.

    Returns:
        list: A list of tuples, where each tuple represents a row from the table.
              Returns an empty list if no records are found or on error.
    """
    records = []
    connection = get_db_connection(mysql_config)
    if connection is None:
        return records

    cursor = None
    try:
        cursor = connection.cursor()
        select_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_query)
        records = cursor.fetchall()
        logger.info(f"Successfully read {len(records)} records from table '{table_name}'.")
    except Error as e:
        logger.error(f"Error reading data from table '{table_name}': {e}")
    finally:
        if cursor:
            cursor.close()
            logger.debug("MySQL cursor closed.")
        if connection and connection.is_connected():
            connection.close()
            logger.debug("MySQL connection closed.")
    return records

