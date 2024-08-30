from datetime import UTC, datetime


from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_socketio import SocketIO

from modules import *

app = Flask(__name__)
socketio = SocketIO(app)

init_db()
start_reminder_checker()
TLE = fetch_tle_data()


@app.route("/")
def index():
    user_id = get_logged_in_user()
    return render_template("index.html", user_id=user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
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
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/iss-now")
def iss_now():
    current_position = get_current_position(TLE)
    return jsonify(current_position)


@app.route("/iss-crew")
def iss_crew():
    iss_crew = get_iss_crew()
    return jsonify(iss_crew[0], iss_crew[1])


@app.route("/future-trajectory")
def future_trajectory():
    start_time = datetime.now(UTC)
    duration = float(
        request.args.get("duration", 3600)
    )  # Default to 1 hour if no duration provided
    interval = 60  # Calculate every 60 seconds
    future_positions = get_future_positions(TLE, start_time, duration, interval)
    return jsonify(future_positions)


@app.route("/iss-info")
def iss_info():
    info = get_iss_info(TLE)
    return jsonify(info)


@app.route("/next-passes", methods=["GET"])
def next_passes():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    if lat is None or lon is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    passes = get_next_passes(TLE, lat, lon, num_passes=3)
    return jsonify(passes)


@app.route("/add-reminder", methods=["POST"])
def add_reminder_route():
    user_id = request.form["user_id"]
    pass_time = request.form[
        "pass_time"
    ]  # Expecting ISO format: '2024-08-30T10:15:00Z'
    add_reminder(user_id, pass_time)

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(debug=False)
