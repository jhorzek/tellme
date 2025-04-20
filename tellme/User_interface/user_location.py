"""Get the users location to find nearby attractions."""

import streamlit as st
from streamlit_js_eval import get_geolocation


def get_user_location() -> dict[str, float]:
    user_location = get_geolocation()
    if user_location is None:
        st.error(
            'Could not get your current location. You can still enter your location manually.'
        )
        current_location = {'latitude': 52.521992, 'longitude': 13.413244}
    else:
        current_location = {
            'latitude': user_location['coords']['latitude'],
            'longitude': user_location['coords']['longitude'],
        }
    return current_location
