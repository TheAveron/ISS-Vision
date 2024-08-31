from typing import Any, Dict, List, Tuple

import requests


def get_iss_crew() -> Tuple[Dict[str, Any], int]:
    """
    Fetch and return the list of crew members currently aboard the ISS.

    Returns:
        Tuple[Dict[str, Any], int]: A tuple where the first element is a dictionary
        containing the list of crew members with the key "crew", and the second
        element is an HTTP status code. The HTTP status code is 200 for successful
        requests and 500 for errors.

    Raises:
        requests.RequestException: If there is an error fetching data from the API.
    """
    try:
        response = requests.get("http://api.open-notify.org/astros.json")
        response.raise_for_status()
        data = response.json()

        # Extract crew members aboard the ISS
        iss_crew: List[Dict[str, Any]] = [
            person for person in data.get("people", []) if person.get("craft") == "ISS"
        ]

        return {"crew": iss_crew}, 200

    except requests.RequestException:
        return {"error": "Error fetching ISS crew data"}, 500
