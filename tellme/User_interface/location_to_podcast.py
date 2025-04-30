from typing import Type

import chatlas
import streamlit as st

from tellme.AI_Podcast.create_podcast_audio import (
    create_podcast_audio_edge,
    create_podcast_audio_openai,
)
from tellme.AI_Podcast.create_podcast_transcript import create_podcast_transcript
from tellme.AI_Podcast.podcast_setups import PodcastHosts


async def location_to_podcast(
    attraction_name: str,
    article: str,
    Chat: Type[chatlas.Chat],
    hosts: PodcastHosts,
    model_name: str,
    api_key: str,
    speech_model: str,
):
    """Create a podcast based on an attraction.

    Args:
        attraction_name (str): Name of the attraction
        article (str): String with the content of the wikipedia article
        Chat (Type[chatlas.Chat]): Chat (Type[chatlas.Chat]): A chat object to call the llm provider
        hosts (PodcastHosts): Podcast host setup
        model_name (str): Name of the llm
        api_key (str): API key for the llm
        speech_model (str): Name of the speech model used to create the voices

    Returns:
        _type_: _description_
    """
    if (api_key is None) | (api_key == ''):
        st.error('Please provide an API key')
        return

    if (api_key is not None) and (api_key != ''):
        pod_transcript = create_podcast_transcript(
            system_prompt=hosts.instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=article,
            api_key=api_key,
        )
    else:
        pod_transcript = create_podcast_transcript(
            system_prompt=hosts.instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=article,
        )

    if Chat == chatlas.ChatOpenAI:
        await create_podcast_audio_openai(
            transcript=pod_transcript,
            output_file=f'{attraction_name}.mp3',
            output_folder='data',
            voices=hosts.voices,
            api_key=api_key,
            speech_model=speech_model,
        )
    else:
        await create_podcast_audio_edge(
            transcript=pod_transcript,
            output_file=f'{attraction_name}.mp3',
            output_folder='data',
            voices=hosts.voices,
        )

    return f'data/{attraction_name}.mp3'
