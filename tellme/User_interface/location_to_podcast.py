import chatlas
import streamlit as st

from tellme.AI_Podcast.create_podcast_audio import (
    create_podcast_audio_edge,
    create_podcast_audio_openai,
)
from tellme.AI_Podcast.create_podcast_transcript import create_podcast_transcript
from tellme.AI_Podcast.podcast_setups import Sofia_Mark


async def location_to_podcast(
    attraction_name,
    article,
    Chat,
    model_name,
    api_key,
    speech_model,
    voice_instructions=Sofia_Mark,
):
    if (api_key is None) | (api_key == ''):
        st.error('Please provide an API key')
        return

    if (api_key is not None) and (api_key != ''):
        pod_transcript = create_podcast_transcript(
            system_prompt=voice_instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=article,
            api_key=api_key,
        )
    else:
        pod_transcript = create_podcast_transcript(
            system_prompt=voice_instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=article,
        )

    if Chat == chatlas.ChatOpenAI:
        await create_podcast_audio_openai(
            transcript=pod_transcript,
            output_file=f'{attraction_name}.mp3',
            output_folder='data',
            voices={'Mark': 'ash', 'Sofia': 'alloy'},
            api_key=api_key,
            speech_model=speech_model,
        )
    else:
        await create_podcast_audio_edge(
            transcript=pod_transcript,
            output_file=f'{attraction_name}.mp3',
            output_folder='data',
            voices={'Mark': 'en-US-RogerNeural', 'Sofia': 'en-GB-SoniaNeural'},
        )

    return f'data/{attraction_name}.mp3'
