# tellme

How to get the project:

1. Download the desktop version of GitHub (this is the easiest way)
2. Open the GitHub desktop app and log in
3. Open the project on GitHub (https://github.com/jhorzek/tellme)
4. Download the project by clicking on Code > Open with GitHub Desktop
5. Open the folder you just downloaded with your editor of choice (e.g., VSCode)

Now that we have the project locally, we have to install all dependencies

First of all, if you want to create a podcast, you will need a few external ressources:

1. install ffmpeg. ffmpeg is required to create audiofiles
2. get an API key for gemini. This is free of charge as long as we are not using too many requests. To this end, go to https://aistudio.google.com/apikey
and create a new API key. Save this API key in a new file called ".env" in the root of the package as `GEMINI_API_KEY=your_api_key`.

So far, we are using edge text to speech. The resulting podcasts sound terrifying, but it's free of charge and therefore a nice tool for
prototyping.

Now, that we have all external dependencies set up, we can get started with the installation of the project itself:

1. Create a new virtual environment with `python -m venv .venv`
2. activate the virtual environment
    - on windows: `.venv\Scripts\activate`
    - on macOS: `source .venv/bin/activate`
3. install poetry: `pip install poetry`
4. install dependencies: `poetry install`

You can now run the scripts.

## How to create a podcast

To get the podcast feature up and running, you will need ffmpeg. Also make sure
that you have tellme installed as well (run `poetry install` in the terminal).

### How to install ffmpeg on windows

Follow the instructions on this website: https://phoenixnap.com/kb/ffmpeg-windows

Once everything is installed, you can create a simple podcast as follows:

```py
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
```