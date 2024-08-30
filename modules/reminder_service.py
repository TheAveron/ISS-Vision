import time
from threading import Thread
from datetime import datetime, timedelta, UTC
import sqlite3
from .database import get_db_connection


def add_reminder(user_id, pass_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO iss_reminders (user_id, pass_time) VALUES (?, ?)",
        (user_id, pass_time),
    )
    conn.commit()
    conn.close()


def reminder_checker():
    while True:

        now = datetime.now(UTC)

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Find reminders that are within the next 10 minutes and haven't been notified
        c.execute(
            """
                SELECT id, user_id, pass_time FROM iss_reminders 
                WHERE notified = 0 AND pass_time <= ?
            """,
            (now,),
        )

        reminders = c.fetchall()

        for reminder in reminders:
            reminder_id, user_id, pass_time = reminder
            # Notify the user (this is a placeholder function)
            notify_user(user_id, pass_time)

            # Mark the reminder as notified
            c.execute(
                """
                    UPDATE iss_reminders SET notified = 1 WHERE id = ?
                """,
                (reminder_id,),
            )

        conn.commit()
        conn.close()
        time.sleep(60)  # Check every minute


def start_reminder_checker():
    # Run reminder checker in a separate thread
    Thread(target=reminder_checker, daemon=True).start()


def notify_user(user_id, pass_time):
    # Implementation to send notification to the user
    print(f"The ISS will pass overhead at {pass_time}")
