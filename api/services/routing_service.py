import requests
from django.conf import settings


ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_route(start_coords, end_coords):

    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start_coords,
            end_coords
        ]
    }

    response = requests.post(
        ORS_URL,
        json=body,
        headers=headers,
        timeout=30
    )

    return response.json()