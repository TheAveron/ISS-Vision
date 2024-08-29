from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db_connection
import sqlite3

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return user[0]  # Return user_id if authentication is successful
    return None

def login_user(user_id):
    session['user_id'] = user_id

def logout_user():
    session.pop('user_id', None)

def get_logged_in_user():
    return session.get('user_id', None)
