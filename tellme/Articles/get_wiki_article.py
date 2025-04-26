import requests


def get_wiki_article(article_id: str, local: str) -> str:
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
