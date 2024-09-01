import os
from datetime import datetime, timezone
from typing import Tuple, Union

from dotenv import load_dotenv
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from werkzeug import Response

from modules import ( fetch_tle_data, get_current_position,
                     get_future_positions, get_iss_crew, get_iss_info,
                     get_logged_in_user, get_next_passes, init_db, login_user,
                     logout_user, register_user,
                     verify_user)

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.getenv("TOKEN")

# Initialize database and start background processes
init_db()
TLE = fetch_tle_data()


@app.route("/")
def index() -> str:
    """
    Renders the home page with the current user's ID.

    Returns:
        str: Rendered HTML template for the index page.
    """
    user_id = get_logged_in_user()
    return render_template("index.html", user_id=user_id)


@app.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    """
    Handles user registration.

    Returns:
        Union[str, Response]: Rendered HTML template for the registration page or redirect to the login page.
    """
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
def login() -> Union[str, Response]:
    """
    Handles user login.

    Returns:
        Union[str, Response]: Rendered HTML template for the login page or redirect to the index page.
    """
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
def logout() -> Response:
    """
    Logs out the current user.

    Returns:
        str: Redirect to the index page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/iss-now")
def iss_now() -> Tuple[Response, int]:
    """
    Returns the current position of the ISS.

    Returns:
        Tuple[Response, int]: JSON response containing the ISS position and HTTP status code.
    """
    current_position = get_current_position(TLE)
    return jsonify(current_position), 200


@app.route("/iss-crew")
def iss_crew() -> Tuple[Response, int]:
    """
    Returns the current crew members on the ISS.

    Returns:
        Tuple[Response, int]: JSON response containing the ISS crew and HTTP status code.
    """
    iss_crew_data, status_code = get_iss_crew()
    return jsonify(iss_crew_data), status_code


@app.route("/future-trajectory")
def future_trajectory() -> Tuple[Response, int]:
    """
    Returns the future trajectory of the ISS.

    Returns:
        Tuple[Response, int]: JSON response containing the future positions and HTTP status code.
    """
    start_time = datetime.now(timezone.utc)
    duration = int(request.args.get("duration", 3600))  # Default to 1 hour
    interval = 60  # Calculate every 60 seconds
    future_positions = get_future_positions(TLE, start_time, duration, interval)
    return jsonify(future_positions), 200


@app.route("/iss-info")
def iss_info() -> Tuple[Response, int]:
    """
    Returns detailed information about the ISS.

    Returns:
        Tuple[Response, int]: JSON response containing the ISS information and HTTP status code.
    """
    info = get_iss_info(TLE)
    return jsonify(info), 200


@app.route("/next-passes", methods=["GET"])
def next_passes() -> Tuple[Response, int]:
    """
    Returns the next passes of the ISS over a given location.

    Returns:
        Tuple[Response, int]: JSON response containing the next passes and HTTP status code.
    """
    lat = request.args.get("lat", type=str)
    lon = request.args.get("lon", type=str)
    if lat is None or lon is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    passes = get_next_passes(TLE, lat, lon, num_passes=3)
    return jsonify(passes), 200

if __name__ == "__main__":
    app.run(debug=False)