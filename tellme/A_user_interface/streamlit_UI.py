import streamlit as st

latitude = st.number_input(
    label = 'latitude'
    , min_value = -90.00000
    , max_value = 90.00000
    , value = None
    , placeholder = '''Enter latitude value of your location'''
)

longitude = st.number_input(
    label = 'latitude'
    , min_value = -180.00000
    , max_value = 180.00000
    , value = None
    , placeholder = '''Enter longitude value of your location'''
)

box_size = st.number_input(
    label = 'Box size'
    , min_value = 1
    , max_value = 100
    , value = 1
    , placeholder = '''Enter size of the box in which you want to search for attractions'''
)

from B_get_location.location import get_bounding_box

bbox = get_bounding_box(latitude, longitude, box_size)
print(bbox.bounds)

st.write(bbox.bounds)