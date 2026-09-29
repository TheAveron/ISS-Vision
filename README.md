# 🛰️ ISS Vision

**A live web tracker for the International Space Station: where it is now, where it's going, and when it passes over you.**

Final project of Harvard's [CS50x](https://cs50.harvard.edu/x/) · Python 3.12 · Flask · SQLite · Leaflet

<!-- TODO: add a screenshot or a short GIF of the main map view -->
![ISS Vision main view](docs/screenshot.png)

🎥 **[Video presentation](https://youtu.be/86QOJ3cgrl4)**

---

## Features

- **Interactive map** (Leaflet + OpenStreetMap) with the ISS's live position, refreshed every 10 seconds.
- **Future trajectory**: the ground track of the next 0 to 12 hours, adjustable with a slider.
- **Layer controls**: show or hide the ISS icon and the trajectory.
- **Live information panel**: altitude, speed and the current crew on board.
- **Pass predictions**: the next three passes over your location, using your browser's geolocation.
- **User accounts**: register and log in to save your map settings (ISS icon, trajectory, trajectory duration and zoom level) and get them back on your next visit.

## How it works

| Part | Implementation |
| --- | --- |
| **Orbit data** | TLE (two-line element set) fetched from [CelesTrak](https://celestrak.org), cached for 24 hours in `tle_cache.txt`, with a built-in fallback TLE if the network fails |
| **Orbit computation** | [PyEphem](https://rhodesmill.org/pyephem/): position, altitude, ground track and pass prediction computed from the TLE |
| **Crew** | [Open Notify](http://open-notify.org/Open-Notify-API/People-In-Space/) API |
| **Backend** | Flask JSON API (`/iss-now`, `/future-trajectory`, `/iss-info`, `/iss-crew`, `/next-passes`) plus routes for accounts and settings |
| **Accounts** | SQLite, passwords hashed with Werkzeug, sessions handled by Flask |
| **Frontend** | Vanilla JavaScript split by feature (`map`, `iss`, `controls`, `info`, `utils`) and modular CSS |

## Project structure

```
ISS-Vision/
├── app.py               # Flask routes only; logic lives in modules/
├── modules/
│   ├── database.py      # SQLite setup and connections
│   ├── iss_tracker.py   # position, ground track, altitude, speed, passes (PyEphem)
│   ├── iss_info.py      # crew on board
│   ├── tle_fetcher.py   # TLE download, cache and fallback
│   └── user_service.py  # registration, login, saved map settings
├── static/
│   ├── js/              # map, iss, controls, info, utils
│   └── css/
├── templates/           # base, index, login, register
└── requirements.txt
```

`app.py` stays as small as possible: every feature lives in its own module, on the Python side and on the JavaScript side.

## Getting started

```bash
git clone https://github.com/TheAveron/ISS-Vision.git
cd ISS-Vision
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "TOKEN=change-me-to-a-long-random-string" > .env   # Flask secret key
python app.py
```

Then open <http://127.0.0.1:5000>. The database is created automatically on first launch.

## Limitations and ideas

- The TLE is refreshed once a day; between reboosts of the station, accuracy stays good, but it does degrade over time.
- Pass predictions give rise and set times only. Adding maximum elevation, duration and a "visible to the naked eye" filter (night-time only) would be a natural next step.
- The trajectory is a ground track sampled every 60 seconds.
- Ideas: a public deployment, notifications before a pass, and a live-updating pass list.

## Credits

Built by [TheAveron](https://github.com/TheAveron) as the final project of CS50x, September 2024. Map data © OpenStreetMap contributors.

## License

MIT
