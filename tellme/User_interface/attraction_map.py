import asyncio

import folium
import streamlit as st
from streamlit_folium import st_folium

from tellme.AI_Summary.summary import create_article_summary
from tellme.Articles.get_wiki_article import get_wiki_article
from tellme.Attractions.get_attractions import (
    Attraction,
    find_nearby_articles,
)
from tellme.User_interface.location_to_podcast import location_to_podcast


def add_podcast(attraction_name, path):
    st.session_state.podcasts[attraction_name] = path


def add_summary(attraction_name, summary_text):
    st.session_state.summary[attraction_name] = summary_text


def get_podcast(attraction_name):
    return st.session_state.podcasts.get(attraction_name)


def get_summary(attraction_name):
    return st.session_state.summary.get(attraction_name)


def show_attraction_details(
    attraction: Attraction, chat_provider: str, Chat, model_name, api_key, speech_model
) -> None:
    # Create a list with each of the locations and allow users to create podcasts
    st.subheader(attraction.name)
    if (api_key is None) or (api_key == ''):
        st.error('Please provide an API key')
        return

    if get_summary(attraction_name=attraction.name):
        st.text(get_summary(attraction_name=attraction.name))
    else:
        summary_text = create_article_summary(
            get_wiki_article(article_title=attraction.name),
            Chat=Chat,
            model=model_name,
            api_key=api_key,
        )

        add_summary(attraction_name=attraction.name, summary_text=summary_text)
        st.text(get_summary(attraction_name=attraction.name))

    if get_podcast(attraction.name):
        st.audio(
            get_podcast(attraction.name),
            format='audio/mpeg',
            loop=False,
            autoplay=False,
        )
    else:
        if st.button(
            'Create Podcast',
            key=f'create_podcast_{attraction.name}_{attraction.wikidata_id}',
        ):
            if (api_key is None) or (api_key == ''):
                st.error('Please provide an API key for Gemini.')
            else:
                with st.spinner('Creating the podcast for you...', show_time=True):
                    pod_path = asyncio.run(
                        location_to_podcast(
                            article=get_wiki_article(article_title=attraction.name),
                            attraction_name=attraction.name,
                            Chat=Chat,
                            model_name=model_name,
                            api_key=api_key,
                            speech_model=speech_model,
                        )
                    )
                add_podcast(attraction.name, pod_path)
                st.audio(
                    get_podcast(attraction.name),
                    format='audio/mpeg',
                    loop=False,
                    autoplay=False,
                )


def show_map(
    latitude,
    longitude,
    attractions: list[Attraction],
    chat_provider,
    Chat,
    model_name,
    api_key,
    speech_model,
):
    map = folium.Map(location=[latitude, longitude], zoom_start=16)
    for attr in attractions:
        folium.Marker(
            [attr.location['latitude'], attr.location['longitude']],
            popup=attr.name,
            tooltip=attr.name,
            icon=folium.Icon(color='green', icon_color='white', icon='info-sign'),
        ).add_to(map)
    # We also want to show the users location:
    folium.Marker(
        [latitude, longitude],
        popup='Your location',
        tooltip='Your location',
        icon=folium.Icon(color='blue', icon_color='white', icon='info-sign'),
    ).add_to(map)
    st_data = st_folium(map, use_container_width=True, width=1200, height=500)
    if st_data['last_object_clicked_tooltip'] is not None:
        for attraction in attractions:
            if attraction.name == st_data['last_object_clicked_tooltip']:
                show_attraction_details(
                    attraction=attraction,
                    chat_provider=chat_provider,
                    Chat=Chat,
                    model_name=model_name,
                    api_key=api_key,
                    speech_model=speech_model,
                )


def fetch_and_create_attraction_map(
    latitude, longitude, radius, chat_provider, Chat, model_name, api_key, speech_model
):
    print(f'Calling find_nearby_articles with {latitude} {longitude} {radius}')
    attractions = find_nearby_articles(
        latitude=latitude, longitude=longitude, radius=radius, max_results=50
    )
    # Show the attractions on a map
    show_map(
        latitude,
        longitude,
        attractions,
        chat_provider=chat_provider,
        Chat=Chat,
        model_name=model_name,
        api_key=api_key,
        speech_model=speech_model,
    )
