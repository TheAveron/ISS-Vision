import sqlite3
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from .database import get_db_connection

def register_user(username, password):
    """
    Registers a new user with a hashed password. Returns True if successful, False if the username already exists.
    """
    try:
        with get_db_connection() as conn:
            hashed_password = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists


def verify_user(username, password):
    """
    Verifies a user's credentials. Returns the user_id if successful, None otherwise.
    """
    query = "SELECT id, password FROM users WHERE username = ?"
    with get_db_connection() as conn:
        user = conn.execute(query, (username,)).fetchone()

    if user and check_password_hash(user[1], password):
        return user[0]  # Return user_id if authentication is successful
    return None


def login_user(user_id):
    """
    Logs in a user by setting the session user_id.
    """
    session["user_id"] = user_id


def logout_user():
    """
    Logs out the current user by removing the user_id from the session.
    """
    session.pop("user_id", None)


def get_logged_in_user():
    """
    Returns the currently logged-in user_id from the session, or None if no user is logged in.
    """
    return session.get("user_id")
