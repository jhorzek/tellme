"""Get the users location to find nearby attractions."""

import streamlit as st
from streamlit_js_eval import get_geolocation


def get_user_location() -> dict[str, float]:
    """Calls javascript library to get the users location.

    Returns:
        dict[str, float]: coordinates (latitude and longitude)
    """
    user_location = get_geolocation()
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
