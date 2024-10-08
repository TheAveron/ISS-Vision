import os
import time
from datetime import datetime, timedelta
from typing import List, Tuple

import requests

# Local backup TLE data
LOCAL_TLE = {
    "name": "ISS",
    "line1": "1 25544U 98067A   24241.03733169  .00022625  00000+0  40054-3 0  9997",
    "line2": "2 25544  51.6393 319.3593 0006301 282.8570 136.4539 15.50177998469691",
}

CACHE_FILE = "tle_cache.txt"  # Path to the cache file
CACHE_EXPIRATION = timedelta(days=1)  # Cache duration


def fetch_tle_data(
    url: str = "https://www.celestrak.com/NORAD/elements/stations.txt",
    retries: int = 3,
    delay: int = 5,
) -> Tuple[str, str, str]:
    """
    Fetch the latest TLE data from the specified URL or use cached data if available and valid.
    If all fetch attempts fail, fallback to local TLE data.

    Args:
        url (str): The URL from which to fetch the TLE data.
        retries (int): The number of retry attempts for fetching the data.
        delay (int): The delay in seconds between retry attempts.

    Returns:
        Tuple[str, str, str]: A tuple containing the TLE name, line1, and line2.

    Raises:
        requests.exceptions.RequestException: If there is an error fetching data from the API.
    """
    if is_cache_valid():
        return read_cached_tle()

    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            tle_data = response.text.splitlines()

            if len(tle_data) >= 3:
                cache_tle_data(tle_data)
                return tle_data[0].strip(), tle_data[1].strip(), tle_data[2].strip()

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)

    print("All attempts failed, using local TLE data.")
    return LOCAL_TLE["name"], LOCAL_TLE["line1"], LOCAL_TLE["line2"]


def is_cache_valid() -> bool:
    """
    Check if the cache file exists and is within the expiration period.

    Returns:
        bool: True if the cache file exists and is still valid, False otherwise.
    """
    if os.path.exists(CACHE_FILE):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        return datetime.now() - file_mod_time < CACHE_EXPIRATION
    return False


def read_cached_tle() -> Tuple[str, str, str]:
    """
    Read the TLE data from the cache file.

    Returns:
        Tuple[str, str, str]: A tuple containing the TLE name, line1, and line2.
    """
    with open(CACHE_FILE, "r") as file:
        tle_data = file.readlines()
        if len(tle_data) >= 3:
            return tle_data[0].strip(), tle_data[1].strip(), tle_data[2].strip()
    return LOCAL_TLE["name"], LOCAL_TLE["line1"], LOCAL_TLE["line2"]


def cache_tle_data(tle_data: List[str]) -> None:
    """
    Cache the TLE data to a file.

    Args:
        tle_data (List[str]): A list containing the TLE data lines.
    """
    with open(CACHE_FILE, "w") as file:
        file.write("\n".join(tle_data[:3]))


if __name__ == "__main__":
    # Example usage
    tle_name, tle_line1, tle_line2 = fetch_tle_data()
    print(tle_name)
    print(tle_line1)
    print(tle_line2)
