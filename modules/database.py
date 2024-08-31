import sqlite3
from typing import Optional

DATABASE_FILE = "database.db"


def init_db() -> None:
    """
    Initializes the database by creating the necessary tables if they do not exist.

    This function creates the `iss_reminders` and `users` tables if they are not already present.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # Create iss_reminders table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS iss_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                pass_time DATETIME,
                notified BOOLEAN DEFAULT 0
            )
            """
        )

        # Create users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        conn.commit()


def get_db_connection() -> sqlite3.Connection:
    """
    Creates and returns a new connection to the database.

    Returns:
        sqlite3.Connection: A new database connection.
    """
    return sqlite3.connect(DATABASE_FILE)
