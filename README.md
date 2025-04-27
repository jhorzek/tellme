# tellme

Discover your surroundings with short podcasts based on Wikipedia articles!

> The app is live at https://tellmemore.streamlit.app/

tellme is a simple podcast AI that is heavily inspired by [podcastfy](https://github.com/souzatharsis/podcastfy). The objective is to search nearby sight seeing spots and generate short podcasts for those spots. The current version is a prototype, but once built into a proper app, this would allow you to discover your city while you are going for a walk.

There are currently two ways to setting everyting up. If you are only interested in running the app, you can use
the docker image at `ghcr.io/jhorzek/tellme:latest`. If you want to contribute to the development of the app, we recommend using the devcontainer with VSCode.

## Using docker to run the app

First, download and install docker. 

When on linux or windows, run:

```
docker run -p 8501:8501 ghcr.io/jhorzek/tellme:latest
```

On mac-os run:

```
docker run --platform linux/amd64 -p 8501:8501 ghcr.io/jhorzek/tellme:latest
```

Go to the browser window indicated in the terminal.

## Contributing to tellme

The easiest way to work with the source code of tellme is to use Github's codespaces. Simply click on the "Code" button on top, select codespaces and click open in codespace. The setup may take a minute, but after that you should have the projects latest version in an online VSCode interface ready to go. To create a podcast, run

```
poetry run streamlit run --server.port=8501 --server.address=0.0.0.0 tellme/User_interface/streamlit_UI.py
```

If you want to develop locally, please:

1. install Docker on your computer
2. install VSCode and the Dev Containers extension
3. Download the project. The Dev Containers extension should automatically detect the docker setup and ask you if it should set up the dev container for you

After a few minutes, you should be ready to code! You can run the application with

```
poetry run streamlit run --server.port=8501 --server.address=0.0.0.0 tellme/User_interface/streamlit_UI.py
```

## API Keys

To use gemini to create podcast scripts, you will need an API key. Google provides a free key that can be used for a small number of requests. Go to https://aistudio.google.com/apikey
and create a new API key. Save this API key and supply it to the app to create a podcast.

So far, we are using edge text to speech. The resulting podcasts sound terrifying, but it's free of charge and therefore a nice tool for
prototyping.
