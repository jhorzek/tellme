from podcastfy.client import generate_podcast
from typing import Optional, Any

def create_podcast(urls: list[str], conversation_config: dict[str, Any] = {"word_count": 500}) -> Optional[str]:
    """Create a podcast from a list of urls to articles.

    This function creates a podcast about a specific topic

    Args:
        urls (list[str]): _description_

    Returns:
        Optional[str]: _description_
    """
    # All we have to do is pass our urls to podcastify:
    audio_file: Optional[str] = generate_podcast(urls=urls, tts_model = "edge", conversation_config=conversation_config)

    # generate_podcast saves a transcript and audio file. It returns the
    # path to the audio file if such a file could be created
    if audio_file is not None:
        print("Audio file created and saved at " + audio_file)

    return audio_file
