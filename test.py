import asyncio

from chatlas import ChatGoogle

from tellme.B_get_location.location import get_bounding_box
from tellme.C_get_attractions_nearby.get_attractions import get_nearby_attractions
from tellme.D_get_article.get_wiki_article import get_wiki_article
from tellme.F_create_podcast.create_podcast_audio import create_podcast_audio_edge
from tellme.F_create_podcast.create_podcast_transcript import (
    create_podcast_transcript,
    get_model_api_key,
)
from tellme.F_create_podcast.podcast_setups import Sofia_Mark

api_key = get_model_api_key(key_name='GEMINI_API_KEY')

# 1km bounding box around Alexanderplatz
bounding_box = get_bounding_box(52.521992, 13.413244, 1.0)
locs = get_nearby_attractions(
    west_longitude=bounding_box.bounds[0],
    south_latitude=bounding_box.bounds[1],
    east_longitude=bounding_box.bounds[2],
    north_latitude=bounding_box.bounds[3],
)

art = get_wiki_article(article_title=locs[0].name)


pod_transcript = create_podcast_transcript(
    system_prompt=Sofia_Mark, Chat=ChatGoogle, wiki_article=art, api_key=api_key
)

asyncio.run(
    create_podcast_audio_edge(
        transcript=pod_transcript,
        output_file='podcast_output.mp3',
        output_folder='data',
        voices={'Mark': 'en-US-RogerNeural', 'Sofia': 'en-GB-SoniaNeural'},
    )
)
