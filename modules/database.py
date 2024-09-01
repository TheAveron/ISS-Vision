import sqlite3
from typing import Optional

DATABASE_FILE = "database.db"


def init_db() -> None:
    """
    Initializes the database by creating the necessary tables if they do not exist.

    This function creates the `users` table if it's not already present.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

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
