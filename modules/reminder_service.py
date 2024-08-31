import sqlite3
from datetime import datetime, timezone
from threading import Timer
from typing import List, Tuple

from flask_socketio import emit

from .database import get_db_connection


def add_reminder(user_id: str, pass_time: datetime) -> None:
    """
    Adds a reminder for a user at a specified pass time.
    Ensures that duplicate reminders are not added.

    Args:
        user_id (str): The ID of the user to whom the reminder will be added.
        pass_time (datetime): The time when the ISS pass is scheduled.
    """
    query = """
        INSERT INTO iss_reminders (user_id, pass_time)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM iss_reminders WHERE user_id = ? AND pass_time = ?
        );
    """
    with get_db_connection() as conn:
        conn.execute(query, (user_id, pass_time, user_id, pass_time))
        conn.commit()


def reminder_checker() -> None:
    """
    Checks for reminders that need to be triggered and notifies users.
    Deletes the reminder after notifying the user.
    """
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    query = """
        SELECT id, user_id, pass_time FROM iss_reminders 
        WHERE notified = 0 AND pass_time <= ?
    """

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(query, (now,))
            reminders: List[Tuple[int, str, datetime]] = cursor.fetchall()

            for reminder_id, user_id, pass_time in reminders:
                notify_user(user_id, pass_time)
                conn.execute("DELETE FROM iss_reminders WHERE id = ?", (reminder_id,))
            conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    # Schedule the next check after 60 seconds
    Timer(60, reminder_checker).start()


def start_reminder_checker() -> None:
    """
    Initiates the reminder checking loop.
    """
    reminder_checker()


def notify_user(user_id: str, pass_time: datetime) -> None:
    """
    Sends a WebSocket notification to the user about the ISS pass time.

    Args:
        user_id (str): The ID of the user to be notified.
        pass_time (datetime): The time when the ISS pass is scheduled.
    """
    emit(
        "reminder",
        {"user_id": user_id, "pass_time": pass_time.isoformat()},
        namespace="/notifications",
    )
    print(f"Notification sent for user {user_id} at {pass_time}")
