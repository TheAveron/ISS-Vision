from datetime import datetime
import time
import threading
from .database import get_db_connection

def add_reminder(user_id, pass_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO iss_reminders (user_id, pass_time) VALUES (?, ?)', (user_id, pass_time))
    conn.commit()
    conn.close()

# Function to send notification (mocked)
def send_notification(user_id, message):
    print(f"Notification to user {user_id}: {message}")

# Background scheduler to check for upcoming passes
def reminder_checker():
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.utcnow()
        cursor.execute('''
            SELECT id, user_id, pass_time FROM iss_reminders 
            WHERE notified = 0 AND pass_time <= ?
        ''', (now,))
        reminders = cursor.fetchall()
        
        for reminder in reminders:
            reminder_id, user_id, pass_time = reminder
            send_notification(user_id, f"The ISS will pass overhead at {pass_time}")
            cursor.execute('UPDATE iss_reminders SET notified = 1 WHERE id = ?', (reminder_id,))
        
        conn.commit()
        conn.close()
        time.sleep(60)  # Check every minute

# Start the background reminder checker in a separate thread
def start_reminder_checker():
    threading.Thread(target=reminder_checker, daemon=True).start()
