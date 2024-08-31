import requests
from flask import Flask, jsonify


def get_iss_crew():
    """
    Fetch and return the list of crew members currently aboard the ISS.
    """
    try:
        response = requests.get("http://api.open-notify.org/astros.json")
        response.raise_for_status()
        data = response.json()

        # Extract crew members aboard the ISS
        iss_crew = [person for person in data.get("people", []) if person.get("craft") == "ISS"]

        return {"crew": iss_crew}, 200

    except requests.RequestException:
        return {"error": "Error fetching ISS crew data"}, 500
