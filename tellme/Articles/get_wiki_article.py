"""Download the contents of a wikipedia article."""

import requests


def get_wiki_article(article_id: str, local: str) -> str:
    """Download the contents of a wikipedia article.

    Args:
        article_id (str): The wikipedia ID of the article
        local (str): The language in which the article is hosted. For example, if an article is
        one the english wikipedia, this should be "en"

    Returns:
        str: The content of the article.
    """
    session = requests.Session()

    url = f'https://{local}.wikipedia.org/w/api.php'
    request_parameters = {
        'action': 'parse',
        'prop': 'wikitext',
        'pageid': article_id,
        'formatversion': 2,
        'format': 'json',
    }

    request_result = session.get(url=url, params=request_parameters).json()

    print(request_result)

    return request_result['parse']['wikitext']
