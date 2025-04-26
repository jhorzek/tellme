"""Streamlit UI."""

import streamlit as st
from chatlas import ChatGoogle, ChatOpenAI

from tellme.User_interface.attraction_map import fetch_and_create_attraction_map
from tellme.User_interface.user_location import get_user_location

# Make sure that the following elements are kept when the app is rerun:
if 'podcasts' not in st.session_state:
    st.session_state.podcasts = {}

if 'summary' not in st.session_state:
    st.session_state.summary = {}

current_location = get_user_location()

with st.sidebar:
    st.header('Location:')
    latitude = st.number_input(
        label='latitude',
        min_value=-90.00000,
        max_value=90.00000,
        value=current_location['latitude'],
        placeholder="""Enter latitude value of your location""",
    )

    longitude = st.number_input(
        label='longitude',
        min_value=-180.00000,
        max_value=180.00000,
        value=current_location['longitude'],
        placeholder="""Enter longitude value of your location""",
    )

    radius = st.number_input(
        label='Radius',
        min_value=1,
        max_value=10000,
        value=1000,
        placeholder="""Enter size of the radius in which you want to search for attractions""",
    )

    st.header('Model Settings')

    chat_provider = st.selectbox(
        'Choose a chat provider', ['Gemini', 'OpenAI'], index=0
    )

    if chat_provider == 'Gemini':
        model_name = st.text_input(
            'Name of the AI model to use', value='gemini-2.0-flash'
        )
        speech_model = 'edge-tts'
    elif chat_provider == 'OpenAI':
        model_name = st.text_input('Name of the AI model to use', value='gpt-4.1')
        st.text('OpenAI will also be used to generate the voices.')
        speech_model = 'gpt-4o-mini-tts'

    api_key = st.text_input(f'Your API Key for {chat_provider}', type='password')

    match chat_provider:
        case 'Gemini':
            Chat = ChatGoogle
        case 'OpenAI':
            Chat = ChatOpenAI


if (latitude is not None) and (longitude is not None) and (radius is not None):
    fetch_and_create_attraction_map(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        chat_provider=chat_provider,
        Chat=Chat,
        model_name=model_name,
        api_key=api_key,
        speech_model=speech_model,
    )
