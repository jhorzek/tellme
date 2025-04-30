"""Get the users location to find nearby attractions."""

import requests
import streamlit as st
from streamlit_js_eval import get_geolocation


def address_to_coordinates(address: str) -> dict[str, float] | None:
    """Retrieve the coordinates based on an address string using https://nominatim.openstreetmap.org/ui/search.html.

    Args:
        address (str): Address description

    Returns:
        dict[str, float]|None: Coordinates or None.
    """
    if (address is None) or (len(address) < 2):
        return None
    session = requests.Session()
    session.headers.update({'User-Agent': 'tellmemore - App'})
    url = 'https://nominatim.openstreetmap.org/search'
    parameters = {'q': address, 'format': 'json'}
    request_result = session.get(url=url, params=parameters).json()
    if len(request_result) > 0:
        result = request_result[0]
        if (result.get('lat') is None) | (result.get('lon') is None):
            return None
        return {
            'latitude': float(result.get('lat')),
            'longitude': float(result.get('lon')),
        }
    else:
        return None


def get_user_location(component_key) -> dict[str, float]:
    """Calls javascript library to get the users location.

    Returns:
        dict[str, float]: coordinates (latitude and longitude)
    """
    user_location = get_geolocation(component_key=component_key)
    if user_location is None:
        st.error(
            'Could not get your current location. You can still enter your location manually.'
        )
        # We set the location to Berlin Weißensee as there are a few attractions around,
        # but not too many so that we don't make lot's of requests to the wikipedia api
        current_location = {'latitude': 52.3315, 'longitude': 13.2751}
    else:
        current_location = {
            'latitude': user_location['coords']['latitude'],
            'longitude': user_location['coords']['longitude'],
        }
    return current_location
