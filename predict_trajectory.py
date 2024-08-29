from datetime import datetime, timedelta

import ephem

# Example TLE data for the ISS
TLE = [
    "1 25544U 98067A   23329.48490253  .00000023  00000-0  18533-4 0  9990",
    "2 25544  51.6442  11.3654 0007307  43.0716 317.0736 15.08743909390888"
]

def get_future_positions(tle, start_time, duration, interval):
    satellite = ephem.readtle('ISS (ZARYA)', tle[0], tle[1])
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

if __name__ == "__main__":
    start_time = datetime.utcnow()
    future_positions = get_future_positions(TLE, start_time, 3600, 60)  # Predict for 1 hour, every 60 seconds
    for pos in future_positions:
        print(pos)
