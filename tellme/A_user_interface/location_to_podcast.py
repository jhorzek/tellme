import asyncio

import streamlit as st
from chatlas import ChatGoogle, ChatOllama

from tellme.C_get_attractions_nearby.get_attractions import get_nearby_attractions
from tellme.D_get_article.get_wiki_article import get_wiki_article
from tellme.F_create_podcast.create_podcast_audio import create_podcast_audio_edge
from tellme.F_create_podcast.create_podcast_transcript import create_podcast_transcript
from tellme.F_create_podcast.podcast_setups import Sofia_Mark


async def location_to_podcast(
    bbox, Chat, model_name, api_key, voice_instructions=Sofia_Mark
):
    locs = get_nearby_attractions(
        west_longitude=bbox.bounds[0],
        south_latitude=bbox.bounds[1],
        east_longitude=bbox.bounds[2],
        north_latitude=bbox.bounds[3],
    )

    if len(locs) == 0:
        st.error('Could not find an attraction nearby')
        return

    art = get_wiki_article(article_title=locs[0].name)

    if (api_key is not None) and (api_key != ''):
        pod_transcript = create_podcast_transcript(
            system_prompt=Sofia_Mark,
            Chat=Chat,
            model=model_name,
            wiki_article=art,
            api_key=api_key,
        )
    else:
        pod_transcript = create_podcast_transcript(
            system_prompt=Sofia_Mark, Chat=Chat, model=model_name, wiki_article=art
        )

    await create_podcast_audio_edge(
        transcript=pod_transcript,
        output_file='podcast_output.mp3',
        output_folder='data',
        voices={'Mark': 'en-US-RogerNeural', 'Sofia': 'en-GB-SoniaNeural'},
    )

    st.audio(
        'data/podcast_output.mp3',
        format='audio/mpeg',
        loop=False,
        autoplay=False,
    )
