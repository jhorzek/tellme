"""Create a summary of a wikipedia article."""

from typing import Type

import chatlas


def create_article_summary(
    wiki_article: str,
    system_prompt: str,
    Chat: Type[chatlas.Chat] = chatlas.ChatGoogle,
    **kwargs,
) -> str:
    """Create the summary of the wikipedia article with AI.

    Args:
        wiki_article (str): Contents of the article from wikipedia
        system_prompt (_type_, optional): System prompt used for the AI when summarizing the article.
        Chat (Type[chatlas.Chat], optional): A chat class from chatlas used to call specific AIs. Defaults to chatlas.ChatGoogle.

    Returns:
        str: A text summary
    """
    chat = Chat(system_prompt=system_prompt, **kwargs)
    summary = chat.chat(wiki_article)

    return summary
