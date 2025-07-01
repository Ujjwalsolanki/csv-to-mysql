# CSV to MySQL ETL Automation

This project provides an automated solution for processing CSV files dropped into a designated folder and storing their data into a MySQL database. It offers two versions for triggering the ETL (Extract, Transform, Load) process: a scheduled task approach and a real-time event-driven approach.

-----

## Features

  * **Automated ETL:** Seamlessly moves data from CSV files to your MySQL database.
  * **Flexible Triggers:** Choose between scheduled processing (Version 1) or real-time processing via file system events (Version 2).
  * **Easy Configuration:** Centralized settings for database connection.

-----

## Getting Started

Follow these steps to get your CSV to MySQL ETL process up and running.

### Prerequisites

Before you begin, ensure you have the following installed:

  * **Python 3.x**
  * **MySQL Server**

### 1\. Database Setup

First, you need to create the necessary database and tables in your MySQL server.

```bash
# Locate the sql.txt file in your project directory
# Execute the SQL commands in sql.txt using a MySQL client (e.g., MySQL Workbench, command line)
mysql -u your_username -p < sql.txt
```

**Note:** Replace `your_username` with your MySQL username. You will be prompted to enter your password.

### 2\. Create a Virtual Environment

It's highly recommended to create a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

### 3\. Activate the Virtual Environment

  * **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
  * **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4\. Install Dependencies

Once your virtual environment is active, install the required Python packages.

```bash
pip install -r requirements.txt
```

### 5\. Configure MySQL Server Settings

You need to provide your MySQL server connection details.

  * Open the file: `config/settings.py`
  * Locate the database configuration section and update it with your MySQL server details (host, user, password, database name).

**Example `config/settings.py` snippet:**

```python
# config/settings.py

MYSQL_CONFIG = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_database_name'
}
```

**Important:** Ensure your MySQL server is running before attempting to run the ETL process.

-----

## Running the ETL Process

This project offers two distinct versions for triggering the ETL process. You'll need to enable one version at a time.

### Version Control

To switch between Version 1 (Task Scheduler) and Version 2 (Watchdog Events), you'll need to modify the `main.py` file.

  * Open `main.py`

  * **To run Version 1:**

      * Uncomment the code block related to Version 1's main function.
      * Comment out the code block related to Version 2's main function.

  * **To run Version 2:**

      * Uncomment the code block related to Version 2's main function.
      * Comment out the code block related to Version 1's main function.

-----

### Version 1: Scheduled ETL (using Task Scheduler)

This version allows you to schedule the ETL process to run at specific intervals using your operating system's task scheduler (e.g., Windows Task Scheduler, Cron on Linux).

1.  **Enable Version 1** in `main.py` as described above.
2.  **Run the script manually** to test:
    ```bash
    python main.py
    ```
3.  **Schedule the script:**
      * **Windows Task Scheduler:** Create a new task that runs `python.exe` from your virtual environment and points to `main.py`.
      * **Cron (Linux/macOS):** Add a cron job entry to execute the script at your desired frequency.

### Version 2: Real-time ETL (using Watchdog Events)

This version uses `watchdog` to monitor the specified folder for new CSV files. As soon as a new file is detected, the ETL process will automatically start.

1.  **Enable Version 2** in `main.py` as described above.
2.  **Run the script:**
    ```bash
    python main.py
    ```
    This will start the file system observer. The script will continue to run and monitor the folder for new CSV files.

-----

## Project Structure

```
.
├── config/
│   └── settings.py             # Database configurations and other settings
├── sql.txt                     # SQL script to create database and tables
├── main.py                     # Main application logic and version control
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── venv/                       # Python virtual environment (created upon setup)
```

-----