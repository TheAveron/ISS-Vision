import sqlite3
from typing import Optional

DATABASE_FILE = "database.db"


def init_db() -> None:
    """
    Initializes the database by creating the necessary tables if they do not exist.

    This function creates the `users` and the `users_settings` table if it's not already present.
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

        # create the users_settings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                toggle_iss BOOLEAN,
                toggle_trajectory BOOLEAN,
                trajectory_time INTEGER,
                zoom_level INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
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
