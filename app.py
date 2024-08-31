import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import (
    Flask, flash, jsonify, redirect, render_template, request,
    session, url_for
)
from flask_socketio import SocketIO
from modules import (
    init_db, start_reminder_checker, fetch_tle_data, get_logged_in_user,
    register_user, verify_user, login_user, logout_user, get_current_position,
    get_iss_crew, get_future_positions, get_iss_info, get_next_passes, add_reminder
)

# Load environment variables
load_dotenv()

# Flask app and SocketIO initialization
app = Flask(__name__)
app.secret_key = os.getenv("TOKEN")
socketio = SocketIO(app)

# Initialize database and start background processes
init_db()
start_reminder_checker()
TLE = fetch_tle_data()

@app.route("/")
def index():
    """Render the home page with the current user's ID."""
    user_id = get_logged_in_user()
    return render_template("index.html", user_id=user_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if register_user(username, password):
            flash("Registration successful, please login.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists. Please choose another.", "danger")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = verify_user(username, password)

        if user_id:
            login_user(user_id)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/iss-now")
def iss_now():
    """Return the current position of the ISS."""
    current_position = get_current_position(TLE)
    return jsonify(current_position)

@app.route("/iss-crew")
def iss_crew():
    """Return the current crew members on the ISS."""
    iss_crew_data, status_code = get_iss_crew()
    return jsonify(iss_crew_data), status_code

@app.route("/future-trajectory")
def future_trajectory():
    """Return the future trajectory of the ISS."""
    start_time = datetime.now(timezone.utc)
    duration = float(request.args.get("duration", 3600))  # Default to 1 hour
    interval = 60  # Calculate every 60 seconds
    future_positions = get_future_positions(TLE, start_time, duration, interval)
    return jsonify(future_positions)

@app.route("/iss-info")
def iss_info():
    """Return detailed information about the ISS."""
    info = get_iss_info(TLE)
    return jsonify(info)

@app.route("/next-passes", methods=["GET"])
def next_passes():
    """Return the next passes of the ISS over a given location."""
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    if lat is None or lon is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    passes = get_next_passes(TLE, lat, lon, num_passes=3)
    return jsonify(passes)

@app.route("/add-reminder", methods=["POST"])
def add_reminder_route():
    """Add a reminder for a specific ISS pass time."""
    user_id = request.form["user_id"]
    pass_time = request.form["pass_time"]  # ISO format: '2024-08-30T10:15:00Z'
    add_reminder(user_id, pass_time)
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(debug=False)
    socketio.run(app)
