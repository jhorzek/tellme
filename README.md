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

Once everything is installed, you can create a simple podcast as follows:

```py
from tellme import create_podcast

audio = create_podcast.create_podcast(["https://de.wikipedia.org/wiki/Nikolaikirche_(Berlin)"])
```