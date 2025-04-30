"""Setup for the AI."""

from typing import Type

from chatlas import Chat

from tellme.AI_Podcast.podcast_setups import PodcastHosts


class SummaryInstructions:
    """Settings for the summary."""

    base_prompt: str

    def __init__(
        self,
        language: str,
        base_instruction: str = 'Please summarize the article with 2 sentences.',
    ):
        """Instructions for the AI generated summary.

        Args:
            language (str): The language in which the summary should be provided.
            base_instruction (str, optional): The instructions for creating the summary. Defaults to "Please summarize the article with 2 sentences.".
        """
        self.base_prompt = (
            base_instruction + f'\nMake sure that the summary is in {language}.'
        )


class PodcastInstructions:
    """Podcast setup."""

    hosts: PodcastHosts

    def __init__(self, hosts: PodcastHosts):
        """Podcast settings.

        Args:
            hosts (PodcastHosts): Hosts of the podcast.
        """
        self.hosts = hosts


class AISettings:
    """General AI settings."""

    Chat: Type[Chat]
    model_name: str
    speech_model: str
    language: str
    summary_instructions: SummaryInstructions
    podcast_instructions: PodcastInstructions
    podcast_generator: str
