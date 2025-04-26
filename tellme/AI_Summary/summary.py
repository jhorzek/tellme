from typing import Type

import chatlas


def create_article_summary(
    wiki_article: str,
    system_prompt: str = 'summarize the article in 2 sentence:',
    Chat: Type[chatlas.Chat] = chatlas.ChatGoogle,
    **kwargs,
):
    chat = Chat(system_prompt=system_prompt, **kwargs)
    summary = chat.chat(wiki_article)

    return summary
