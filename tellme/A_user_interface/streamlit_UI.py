"""Streamlit UI."""

import asyncio

import streamlit as st
from chatlas import ChatGoogle, ChatOllama
from tellme.A_user_interface.location_to_podcast import location_to_podcast
from tellme.B_get_location.location import get_bounding_box

with st.sidebar:
    st.header('Model Settings')

    chat_provider = st.selectbox(
        'Choose a chat provider', {'Gemini', 'Ollama'}, index=0
    )

    if chat_provider == 'Gemini':
        model_name = st.text_input(
            'Name of the AI model to use', value='gemini-2.0-flash'
        )
    else:
        model_name = st.text_input('Name of the AI model to use', value=None)

    if chat_provider == 'Ollama':
        api_key = None
    else:
        api_key = st.text_input(f'Your API Key for {chat_provider}', type='password')

    match chat_provider:
        case 'Gemini':
            Chat = ChatGoogle
        case 'Ollama':
            Chat = ChatOllama

latitude = st.number_input(
    label='latitude',
    min_value=-90.00000,
    max_value=90.00000,
    value=52.521992,
    placeholder="""Enter latitude value of your location""",
)

longitude = st.number_input(
    label='longitude',
    min_value=-180.00000,
    max_value=180.00000,
    value=13.413244,
    placeholder="""Enter longitude value of your location""",
)

box_size = st.number_input(
    label='Box size',
    min_value=1,
    max_value=100,
    value=1,
    placeholder="""Enter size of the box in which you want to search for attractions""",
)

if (latitude is not None) and (longitude is not None) and (box_size is not None):
    bbox = get_bounding_box(latitude, longitude, box_size)

# Add a button
if st.button('Create Podcast'):
    if (latitude is None) or (longitude is None) or (box_size is None):
        st.error(
            'Please provide latitude, longitude, and the box size to create a podcast.'
        )
    elif (chat_provider == 'Gemini') & ((api_key is None) or (api_key == '')):
        st.error('Please provide an API key for Gemini.')
    else:
        asyncio.run(
            location_to_podcast(
                bbox=bbox, Chat=Chat, model_name=model_name, api_key=api_key
            )
        )
