"""Extract all attractions around a location."""

# Adapted from https://www.mediawiki.org/wiki/API:Geosearch/Sample_code_1
import requests
import streamlit as st


class Attraction:
    """An attraction with name, location, wikipedia link and wikidata id."""

    name: str
    location: dict[str, float] = {'latitude': None, 'longitude': None}
    wikipedia_link: str
    wikidata_id: str

    def __init__(
        self,
        name: str,
        location: dict[str, float],
        wikipedia_link: str,
        wikidata_id: str,
    ):
        """Create a new attraction.

        Args:
            name (str): The name of the attraction
            location (dict[str, float]): the location as dict with structure {"latitude": 123.0, "longitude": 345.0}
            wikipedia_link (str): Link to the wikipedia article
            wikidata_id (str): ID of the wikipedia article
        """
        self.name = name
        self.location = location
        self.wikipedia_link = wikipedia_link
        self.wikidata_id = wikidata_id


@st.cache_data
def find_nearby_articles(
    latitude: float,
    longitude: float,
    max_results: int,
    radius: int,
    local: str = 'en',
) -> list[Attraction]:
    """Retrieve articles from wikipedia surrounding a location.

    Args:
        latitude (float): location latitude
        longitude (float): location longitude
        max_results (int): maximal number of results to return
        radius (int): radius surrouding the current location
        local (str, optional): The language of wikipedia to search in. Defaults to 'en'.

    Returns:
        list[Attraction]: A list of attractions. See Attraction for more details
    """
    session = requests.Session()

    url = f'https://{local}.wikipedia.org/w/api.php'
    request_parameters = {
        'action': 'query',
        'list': 'geosearch',
        'gscoord': f'{latitude}|{longitude}',
        'gsradius': radius,
        'gslimit': max_results,
        'format': 'json',
    }

    request_result = session.get(url=url, params=request_parameters).json()

    pages = request_result['query']['geosearch']
    print(f'Found {len(pages)} attractions!')
    attractions = pages_to_attractions(pages=pages)
    return attractions


def pages_to_attractions(pages: list) -> list[Attraction]:
    """Extract the attraction information from wikipedia pages.

    Args:
        pages (list): Pages from wiki request

    Returns:
        list[Attraction]: A list of attractions. See Attraction for more details
    """
    attractions: list[Attraction] = []

    for page in pages:
        name = page['title']
        location = {
            'latitude': float(page['lat']),
            'longitude': float(page['lon']),
        }
        attractions.append(
            Attraction(
                name=name,
                location=location,
                wikipedia_link=f'https://wikipedia.org/wiki/{page["pageid"]}',
                wikidata_id=page['pageid'],
            )
        )
    return attractions
