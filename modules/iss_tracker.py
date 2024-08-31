from datetime import datetime, timedelta, timezone
import ephem


def observer_setup(lat="40.7128", lon="-74.0060", elevation=10):
    """
    Set up an observer with given latitude, longitude, and elevation.
    """
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = elevation
    observer.date = datetime.now(timezone.utc)
    return observer


def get_current_position(tle):
    """
    Get the current latitude and longitude of the satellite.
    """
    observer = observer_setup()
    satellite = ephem.readtle(*tle)
    satellite.compute(observer)
    return {
        "lat": satellite.sublat * 180.0 / ephem.pi,
        "lon": satellite.sublong * 180.0 / ephem.pi,
    }


def get_future_positions(tle, start_time, duration, interval):
    """
    Get satellite positions at regular intervals over a specified duration.
    """
    satellite = ephem.readtle(*tle)
    positions = []
    current_time = start_time

    while current_time <= start_time + timedelta(seconds=duration):
        satellite.compute(current_time)
        positions.append({
            "lat": satellite.sublat * 180.0 / ephem.pi,
            "lon": satellite.sublong * 180.0 / ephem.pi,
        })
        current_time += timedelta(seconds=interval)

    return positions


def get_iss_info(tle):
    """
    Get current information about the ISS including position, altitude, and speed.
    """
    observer = observer_setup()
    satellite = ephem.readtle(*tle)
    satellite.compute(observer)

    return {
        "latitude": satellite.sublat * 180.0 / ephem.pi,
        "longitude": satellite.sublong * 180.0 / ephem.pi,
        "altitude": round(satellite.elevation / 1000.0, 2),  # Convert to km
        "speed": round(abs(satellite.range_velocity) / 1000.0 * 3600.0, 2),  # Convert to km/h
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def get_next_passes(tle, observer_lat, observer_lon, num_passes=3):
    """
    Get the next passes of the ISS over a specified observer location.
    """
    observer = observer_setup(lat=observer_lat, lon=observer_lon)
    satellite = ephem.readtle(*tle)
    passes = []

    for _ in range(num_passes):
        next_pass = observer.next_pass(satellite)
        passes.append({
            "rise_time": next_pass[0].datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "set_time": next_pass[4].datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
        })
        observer.date = next_pass[4] + ephem.minute  # Move time forward

    return passes
