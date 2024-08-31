from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Union

import ephem


def observer_setup(
    lat: str = "40.7128", lon: str = "-74.0060", elevation: int = 10
) -> ephem.Observer:
    """
    Set up an observer with given latitude, longitude, and elevation.

    Args:
        lat (str): Latitude of the observer in decimal degrees.
        lon (str): Longitude of the observer in decimal degrees.
        elevation (int): Elevation of the observer in meters.

    Returns:
        ephem.Observer: An observer object configured with the given parameters.
    """
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = elevation
    observer.date = datetime.now(timezone.utc)
    return observer


def get_current_position(tle: Tuple[str, str, str]) -> Dict[str, float]:
    """
    Get the current latitude and longitude of the satellite.

    Args:
        tle (Tuple[str, str, str]): Tuple containing the TLE (Two-Line Element) data.

    Returns:
        Dict[str, float]: A dictionary containing the latitude and longitude of the satellite.
    """
    observer = observer_setup()
    satellite = ephem.readtle(*tle)
    satellite.compute(observer)
    return {
        "lat": satellite.sublat * 180.0 / ephem.pi,
        "lon": satellite.sublong * 180.0 / ephem.pi,
    }


def get_future_positions(
    tle: Tuple[str, str, str], start_time: datetime, duration: int, interval: int
) -> List[Dict[str, float]]:
    """
    Get satellite positions at regular intervals over a specified duration.

    Args:
        tle (Tuple[str, str, str]): Tuple containing the TLE data.
        start_time (datetime): The starting time for position calculations.
        duration (int): Duration for which to calculate positions, in seconds.
        interval (int): Interval between position calculations, in seconds.

    Returns:
        List[Dict[str, float]]: A list of dictionaries, each containing latitude and longitude of the satellite.
    """
    satellite = ephem.readtle(*tle)
    positions = []
    current_time = start_time

    while current_time <= start_time + timedelta(seconds=duration):
        satellite.compute(current_time)
        positions.append(
            {
                "lat": satellite.sublat * 180.0 / ephem.pi,
                "lon": satellite.sublong * 180.0 / ephem.pi,
            }
        )
        current_time += timedelta(seconds=interval)

    return positions


def get_iss_info(tle: Tuple[str, str, str]) -> Dict[str, Union[float, str]]:
    """
    Get current information about the ISS including position, altitude, and speed.

    Args:
        tle (Tuple[str, str, str]): Tuple containing the TLE data.

    Returns:
        Dict[str, Union[float, str]]: A dictionary containing latitude, longitude, altitude, speed, and timestamp of the ISS.
    """
    observer = observer_setup()
    satellite = ephem.readtle(*tle)
    satellite.compute(observer)

    return {
        "latitude": satellite.sublat * 180.0 / ephem.pi,
        "longitude": satellite.sublong * 180.0 / ephem.pi,
        "altitude": round(satellite.elevation / 1000.0, 2),  # Convert to km
        "speed": round(
            abs(satellite.range_velocity) / 1000.0 * 3600.0, 2
        ),  # Convert to km/h
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def get_next_passes(
    tle: Tuple[str, str, str], observer_lat: str, observer_lon: str, num_passes: int = 3
) -> List[Dict[str, str]]:
    """
    Get the next passes of the ISS over a specified observer location.

    Args:
        tle (Tuple[str, str, str]): Tuple containing the TLE data.
        observer_lat (str): Latitude of the observer in decimal degrees.
        observer_lon (str): Longitude of the observer in decimal degrees.
        num_passes (int): Number of passes to return.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing rise and set times of the ISS.
    """
    observer = observer_setup(lat=observer_lat, lon=observer_lon)
    satellite = ephem.readtle(*tle)
    passes = []

    for _ in range(num_passes):
        next_pass = observer.next_pass(satellite)
        passes.append(
            {
                "rise_time": next_pass[0].datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "set_time": next_pass[4].datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
            }
        )
        observer.date = next_pass[4] + ephem.minute  # Move time forward

    return passes
