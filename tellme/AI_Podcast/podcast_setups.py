"""Defines some setups for the podcast to be used as base prompts for the AI."""


class PodcastHosts:
    """Podcast host setup."""

    names: list[str]
    voices: list[str]
    instructions = str

    def __init__(self, names: list[str], voices: dict[str, str], instructions=str):
        """Create a new podcast hosts setup.

        Args:
            names (list[str]): The names of the hosts
            voices (dict[str, str]): The names of the voices to use
            instructions (str): The instructions to send to the llm
        """
        if len(names) != len(voices):
            raise ValueError('names and voices must have the same length.')
        for name in names:
            if voices.get(name) is None:
                raise ValueError('Could not find a voice for ' + name + '.')

        self.names = names
        self.voices = voices
        self.instructions = instructions


class SofiaMark(PodcastHosts):
    names = ['Sofia', 'Mark']
    instructions = instructions = """
Create a short, engaging podcast transcript between two hosts based on the article below. 
The podcast should feel conversational and friendly, with natural back-and-forth dialogue. 
Keep the total transcript to around 3 minutes in length (approximately 400–450 words).
Make sure to stay very close to the article in terms of content. Do not add more details
that are not mentioned in the article!

## Hosts:

- Sofia (she/her) – Sofia is the explainer. She is thoughtful, confident, and good at breaking down complex ideas into simple, relatable insights. She drives the conversation by summarizing key points from the article and introducing new facts. Her tone is warm and informed, with a natural flow.
- Mark (he/him) – Mark is reactive and expressive. He brings personality and humor to the conversation. He asks questions, offers reactions, and shares personal or broader reflections on the topic. His tone is light, curious, and slightly irreverent.

## Goals:

- Summarize and discuss the article in an engaging, natural-sounding conversation.
- Rephrase content from the article in your own words—no direct quotes.
- Include one surprising or standout fact, twist, or insight from the article.
- Use a conversational, relaxed tone and keep responses short (2–3 sentences per turn).
- End with a brief reflection, question, or takeaway for the listener.
- Stay within the 3-minute time limit (about 400–450 words total).

## Structure:

### Intro (15–20 seconds)

- Both hosts greet the audience.
- Sofia briefly introduces the topic and teases why it’s interesting.

### Main Discussion (2 minutes)

- Sofia explains key parts of the article in segments.
- Mark reacts, comments, adds personality or asks questions.
- Highlight a surprising or memorable insight.

Wrap-Up (30 seconds)

- Mark offers a takeaway or opinion.
- Sofia wraps up with a final thought or question for the listener.
- Friendly sign-off.

### Guidelines:

- Use natural dialogue and avoid sounding robotic or overly formal.
- Avoid long monologues—keep turns snappy and conversational.
- Use plain, accessible language.
- Do not exceed 450 words.
"""

    def __init__(self, voices: dict[str, str], language: str):
        """Initialize podcast with Sofia and Mark.

        Args:
            voices (dict[str, str]): Voices used for Sofia and Mark
            language (str): The language of the podcast

        Raises:
            ValueError: Raises error in case one of the voices is missing
            ValueError: Raises error in case the keys of the dict do not match the names
        """
        if len(self.names) != len(voices):
            raise ValueError('names and voices must have the same length.')
        for name in self.names:
            if voices.get(name) is None:
                raise ValueError('Could not find a voice for ' + name + '.')
        self.voices = voices

        self.instructions = (
            self.instructions
            + f'\n\nPlease make sure that the podcast is in the following language: {language}'
        )
