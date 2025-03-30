"""Generate a podcast from a list of links."""

from typing import Any, Optional

from podcastfy.client import generate_podcast


def create_podcast(
    urls: list[str],
    tts_model: str = 'edge',
    conversation_config: dict[str, Any] = {'word_count': 500},
) -> Optional[str]:
    """Create a podcast from a list of urls to articles.

    This function creates a podcast about a specific topic

    Args:
        urls (list[str]): a list of urls (e.g., urls = ["https://de.wikipedia.org/wiki/Nikolaikirche_(Berlin)"])
        tts_model (str): the name of the text to speech model that podcastfy should use.
            See https://github.com/souzatharsis/podcastfy/blob/59563ee105a0d1dbb46744e0ff084471670dd725/usage/config.md for more details
        conversation_config (dict[str, Any]): A dictionary specifying parameters passed to
            the conversation generator. For example, this can be used to reduce the length of the podcast.

    Returns:
        Optional[str]: if the podcast could be created, a string with the path to the .mp3 file will be returned. Otherwise None.
    """
    # All we have to do is pass our urls to podcastify:
    audio_file: Optional[str] = generate_podcast(
        urls=urls, tts_model=tts_model, conversation_config=conversation_config
    )

    # generate_podcast saves a transcript and audio file. It returns the
    # path to the audio file if such a file could be created
    if audio_file is not None:
        print('Audio file created and saved at ' + audio_file)

    return audio_file
