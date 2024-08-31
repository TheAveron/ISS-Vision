import sqlite3
from typing import Optional

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db_connection


def register_user(username: str, password: str) -> bool:
    """
    Registers a new user with a hashed password.

    Args:
        username (str): The username of the new user.
        password (str): The password for the new user.

    Returns:
        bool: True if registration is successful, False if the username already exists.
    """
    try:
        with get_db_connection() as conn:
            hashed_password = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists


def verify_user(username: str, password: str) -> Optional[int]:
    """
    Verifies a user's credentials.

    Args:
        username (str): The username of the user.
        password (str): The password for the user.

    Returns:
        Optional[int]: The user ID if authentication is successful, None otherwise.
    """
    query = "SELECT id, password FROM users WHERE username = ?"
    with get_db_connection() as conn:
        user = conn.execute(query, (username,)).fetchone()

    if user and check_password_hash(user[1], password):
        return user[0]  # Return user_id if authentication is successful
    return None


def login_user(user_id: int) -> None:
    """
    Logs in a user by setting the session user_id.

    Args:
        user_id (int): The ID of the user to log in.
    """
    session["user_id"] = user_id


def logout_user() -> None:
    """
    Logs out the current user by removing the user_id from the session.
    """
    session.pop("user_id", None)


def get_logged_in_user() -> Optional[int]:
    """
    Returns the currently logged-in user_id from the session.

    Returns:
        Optional[int]: The user ID if logged in, None otherwise.
    """
    return session.get("user_id")
