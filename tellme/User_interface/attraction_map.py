"""Generates a map of nearby attractions."""

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
from tellme.Settings.AI_settings import AISettings
from tellme.User_interface.location_to_podcast import location_to_podcast


def add_podcast(attraction_name: str, path: str):
    """Add a podcast to the list of podcasts saved by tellme.

    Args:
        attraction_name (str): The name of the attraction
        path (str): The path to the podcast mp3 file
    """
    st.session_state.podcasts[attraction_name] = path


def add_summary(attraction_name: str, summary_text: str):
    """Save a summary in the list of summaries.

    Args:
        attraction_name (str): Name of the attraction
        summary_text (str): Summary text
    """
    st.session_state.summary[attraction_name] = summary_text


def get_podcast(attraction_name: str) -> str | None:
    """Retrieve the location of the mp3 file of a podcast.

    Args:
        attraction_name (str): Name of the attraction

    Returns:
        str|None: File path to the mp3 or None if no podcast exists
    """
    return st.session_state.podcasts.get(attraction_name)


def get_summary(attraction_name: str) -> str | None:
    """Retrieve the summary of the article.

    Args:
        attraction_name (str): Name of the attraction

    Returns:
        str|None: Summary of the article or None if no summary exists
    """
    return st.session_state.summary.get(attraction_name)


def wiki_summary(
    attraction: Attraction,
    local: str,
    ai_settings: AISettings,
    api_key: str,
) -> None:
    """Generate and show the wiki-summary.

    Args:
        attraction (Attraction): The attraction for which the article should be summarized
        local (str): The language of the wikipedia article
        ai_settings (AISettings): Settings for the LLMs
        api_key (str): API key for the llm
    """
    if get_summary(attraction_name=attraction.name):
        st.text(get_summary(attraction_name=attraction.name))
    else:
        try:
            article = get_wiki_article(article_id=attraction.wikidata_id, local=local)
        except Exception as error:
            print('Could not retrieve article from wikipedia:', error)
            st.error('Could not retrieve article from wikipedia')
            return
        summary_text = create_article_summary(
            wiki_article=article,
            system_prompt=ai_settings.summary_instructions.base_prompt,
            Chat=ai_settings.Chat,
            model=ai_settings.model_name,
            api_key=api_key,
        )
        summary_text = (
            str(summary_text)
            + f'\n\nThis summary was created based on the wikipedia article on {attraction.name}'
        )

        add_summary(attraction_name=attraction.name, summary_text=summary_text)
        st.text(get_summary(attraction_name=attraction.name))


def podcast(
    attraction: Attraction,
    local: str,
    ai_settings: AISettings,
    api_key: str,
) -> None:
    """Generate and show the podcast.

    Args:
        attraction (Attraction): The attraction for which the article should be summarized
        local (str): The language of the wikipedia article
        Chat (Type[chatlas.Chat]): A chat object to call the llm provider
        hosts (PodcastHosts): Podcast host setup
        model_name (str): Name of the llm
        api_key (str): API key for the llm
        speech_model (str): Name of the speech model
    """
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
                try:
                    article = get_wiki_article(
                        article_id=attraction.wikidata_id, local=local
                    )
                except Exception as error:
                    print('Could not retrieve article from wikipedia:', error)
                    st.error('Could not retrieve article from wikipedia')
                    return
                with st.spinner('Creating the podcast for you...', show_time=True):
                    pod_path = asyncio.run(
                        location_to_podcast(
                            article=article,
                            attraction_name=attraction.name,
                            Chat=ai_settings.Chat,
                            hosts=ai_settings.podcast_instructions.hosts,
                            model_name=ai_settings.model_name,
                            api_key=api_key,
                            speech_model=ai_settings.speech_model,
                        )
                    )
                add_podcast(attraction.name, pod_path)
                st.audio(
                    get_podcast(attraction.name),
                    format='audio/mpeg',
                    loop=False,
                    autoplay=False,
                )


def show_attraction_details(
    attraction: Attraction,
    local: str,
    ai_settings: AISettings,
    api_key: str,
) -> None:
    """Show the summary and the podcast feature for a given attraction.

    Args:
        attraction (Attraction): The attraction for which the article should be summarized
        local (str): The language of the wikipedia article
        ai_settings (AISettings): Settings for the LLMs
        api_key (str): API key for the llm
    """
    # Create a list with each of the locations and allow users to create podcasts
    st.subheader(attraction.name)
    if (api_key is None) or (api_key == ''):
        st.error('Please provide an API key')
        return

    wiki_summary(
        attraction=attraction,
        local=local,
        ai_settings=ai_settings,
        api_key=api_key,
    )

    podcast(
        attraction=attraction,
        local=local,
        ai_settings=ai_settings,
        api_key=api_key,
    )


def show_map(
    latitude: float,
    longitude: float,
    attractions: list[Attraction],
    local: str,
    chat_provider: str,
    ai_settings: AISettings,
    api_key: str,
) -> None:
    """Show the map with the wikipedia articles.

    Args:
        latitude (float): latitude
        longitude (float): longitude
        attractions (list[Attraction]): list with attractions
        local (str): The language of the wikipedia article
        chat_provider (str): Name of the chat provider
        ai_settings (AISettings): Settings for the LLMs
        api_key (str): API key for the llm
    """
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
                    local=local,
                    ai_settings=ai_settings,
                    api_key=api_key,
                )


def fetch_and_create_attraction_map(
    local: str,
    latitude: float,
    longitude: float,
    radius: float,
    chat_provider: str,
    ai_settings: AISettings,
    api_key: str,
) -> None:
    """Fetch local attractions and fill map.

    Args:
        local (str): The language of the wikipedia article
        latitude (float): latitude
        longitude (float): longitude
        radius (float): radius around latitude / longitude in which attractions should be searched
        chat_provider (str): Name of the chat provider
        ai_settings (AISettings): Setting for the LLMs
        api_key (str): API key for the llm
    """
    print(f'Calling find_nearby_articles with {latitude} {longitude} {radius}')
    attractions = find_nearby_articles(
        local=local,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        max_results=50,
    )
    # Show the attractions on a map
    show_map(
        latitude,
        longitude,
        attractions,
        local=local,
        chat_provider=chat_provider,
        ai_settings=ai_settings,
        api_key=api_key,
    )
