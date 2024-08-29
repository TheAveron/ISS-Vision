import time

import requests

# Local backup TLE data
local_tle_name = "ISS"
local_line1 = "1 25544U 98067A   24241.03733169  .00022625  00000+0  40054-3 0  9997"
local_line2 = "2 25544  51.6393 319.3593 0006301 282.8570 136.4539 15.50177998469691"

def fetch_tle_data(url="https://www.celestrak.com/NORAD/elements/stations.txt", retries=1, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            tle_data = response.text.splitlines()
            return tle_data[0].strip(), tle_data[1].strip(), tle_data[2].strip()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("All attempts failed, using local TLE data.")
                return local_tle_name, local_line1, local_line2
