import sqlite3

DATABASE_FILE = "database.db"

def init_db():
    """
    Initializes the database by creating the necessary tables if they do not exist.
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


def get_db_connection():
    """
    Returns a new connection to the database.
    """
    return sqlite3.connect(DATABASE_FILE)
