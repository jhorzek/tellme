"""Create a transcript for a podcast."""

import os
from typing import Type

import chatlas
from pydantic import BaseModel, Field


def get_model_api_key(key_name: str) -> str:
    """Extract an API key from a .env file.

    Many of the AI models require an API key. This function exports that API
    key from the environment variables.

    Args:
        key_name (str): The name of the key in the environment variables file

    Returns:
        str: The api key

    Example:
        from tellme.F_create_podcast.create_podcast_transcript import get_model_api_key
        get_model_api_key("GEMINI_API_KEY")
    """
    # The model api key should be at the root of the project in a .env file
    api_key = os.environ.get(key_name)
    if not api_key:
        raise ValueError(f'Environment variable {key_name} not found.')
    return api_key


class Utterance(BaseModel):
    """An utterance is a single statement by one of the speakers.

    An utterance has the fields "name" (name of the speaker) and "utterance" (what
    was said).

    Args:
        BaseModel: BaseModel
    """

    speaker: str = Field(
        description='The name of the speaker making the current utterance.'
    )
    utterance: str = Field(description='The utterance of the current speaker.')


class Transcript(BaseModel):
    """Transcript of the podcast.

    This class is used by chatlas to export structured data from gemini or other AI
    models that support it.

    Args:
        BaseModel: BaseModel
    """

    utterances: list[Utterance]


def create_podcast_transcript(
    system_prompt: str, wiki_article: str, Chat: Type[chatlas.Chat], **kwargs
) -> list[dict[str, str]]:
    """Create the transcript for a podcast.

    A transcript is a list of utterances by the hosts of the podcast. Each utterance
    has the name of the host and the statements made.

    Args:
        system_prompt (str): This prompt outlines the instructions given for generating
            the podcast. It should describe in detail which hosts there are, what style the
            conversation should have, etc.
        wiki_article (str): The text of the wikipedia article that should be discussed
            in the podcast.
        Chat (Type[chatlas.Chat]): A class from chatlas that is used to generate the
            podcast (e.g., chatlas.ChatGoogle for Gemini).
        **kwargs: Additional arguments passed to Chat. For example, chatlas.ChatGoogle
            required an API key.

    Returns:
        Transcript: A list of utterances. Each element has a speaker and an utterance
            field.

    Example:
        from tellme.F_create_podcast.create_podcast_transcript import create_podcast_transcript
        from tellme.F_create_podcast.podcast_setup import Sofia_Mark_tts
        from chatlas import ChatGoogle
        create_podcast_transcript(system_prompt = Sofia_Mark_tts.instructions,
                                  wiki_article = "this is a placeholder for the article text",
                                  Chat = ChatGoogle,
                                  api_key = "your_api_key")
    """
    chat = Chat(
        system_prompt=system_prompt,
        **kwargs,
    )
    transcript = chat.extract_data(
        '\n\nPlease now create a podcast based on the following article:\n\n'
        + wiki_article
        + '\n\nMake sure to mention that it is an article from wikipedia and that the podcast is ai generated.',
        data_model=Transcript,
    )
    return transcript['utterances']
