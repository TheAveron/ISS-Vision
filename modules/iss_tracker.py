from datetime import UTC, datetime, timedelta

import ephem


def observer_setup(lat = "40.7128", lon = "-74.0060"):
    # Create an Observer object
    observer = ephem.Observer()

    # Set the observer's location
    observer.lat = lat
    observer.lon = lon  
    observer.elevation = 10

    observer.date = datetime.now(UTC)

    return observer

def get_current_position(tle):
    satellite = ephem.readtle(tle[0], tle[1], tle[2])
    satellite.compute(observer_setup())
    return {
        'lat': satellite.sublat * 180.0 / ephem.pi,
        'lon': satellite.sublong * 180.0 / ephem.pi
    }

def get_future_positions(tle, start_time, duration, interval):
    satellite = ephem.readtle(tle[0], tle[1], tle[2])
    positions = []
    current_time = start_time

    while current_time <= start_time + timedelta(seconds=duration):
        satellite.compute(current_time)
        positions.append({
            'lat': satellite.sublat * 180.0 / ephem.pi,
            'lon': satellite.sublong * 180.0 / ephem.pi
        })
        current_time += timedelta(seconds=interval)

    return positions

def get_iss_info(tle):
    # Create a satellite object from the TLE data
    satellite = ephem.readtle(tle[0], tle[1], tle[2])
    
    # Compute the current position of the satellite
    satellite.compute(observer_setup())  # Use the current UTC time

    # Get latitude and longitude of the ISS
    latitude = satellite.sublat * 180.0 / ephem.pi  # Convert from radians to degrees
    longitude = satellite.sublong * 180.0 / ephem.pi  # Convert from radians to degrees

    # Calculate altitude in kilometers
    altitude_km = satellite.elevation / 1000.0  # ephem returns elevation in meters
    
    # Calculate speed in km/h
    speed_kmh = abs(satellite.range_velocity / 1000.0 * 3600.0)  # ephem returns range_velocity in m/s

    # Return the data as JSON
    return {
        'latitude': latitude,
        'longitude': longitude,
        'altitude':  round(altitude_km,2),
        'speed': round(speed_kmh,2),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

def get_next_passes(tle, observer_lat, observer_lon, num_passes=3):
    iss = ephem.readtle(tle[0], tle[1], tle[2])

    Paris = {
        "lat": "48.864716",
        "Lon": "2.349014",
    }
    observer = observer_setup(Paris["lat"], Paris['Lon'])

    passes = []
    for _ in range(num_passes):
        next_pass = observer.next_pass(iss)
        print(next_pass)
        passes.append({
            'rise_time': next_pass[0].datetime().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'set_time': next_pass[4].datetime().strftime('%Y-%m-%d %H:%M:%S UTC')
        })
        observer.date = next_pass[4] + ephem.minute  # Move time forward

    return passes