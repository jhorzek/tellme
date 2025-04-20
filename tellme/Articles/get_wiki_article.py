import wikipedia


def get_wiki_article(article_title: str) -> str:
    wikisearch = wikipedia.page(title=article_title)
    wikicontent = wikisearch.content
    return wikicontent
