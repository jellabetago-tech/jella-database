
import os

import mysql.connector
from mysql.connector import Error

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "portfolio_db"),
}


def get_connection():
    """Open a connection to the local XAMPP MySQL server."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if not connection.is_connected():
            print("[DB] Connection was created but is not active.")
            connection.close()
            return None
        return connection
    except Error as error:
        print(f"[DB] Connection error: {error}")
        return None


def test_connection():
    connection = get_connection()
    if connection is not None:
        print("[DB] Connected to XAMPP MySQL successfully.")
        connection.close()
        return True
    print("[DB] Could not connect. Check that MySQL is running in XAMPP and the database exists.")
    return False


def main():
    test_connection()


if __name__ == "__main__":
    main()