"""Extract all attractions within a bounding box."""

import overpy


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


def get_nearby_attractions(
    west_longitude: float,
    south_latitude: float,
    east_longitude: float,
    north_latitude: float,
) -> list[Attraction]:
    """Retrieve all attractions within a given bounding box.

    All nodes with the tag ["tourism"="attraction"] and a wikipedia article
    are returned.

    Args:
        west_longitude (float): The western longitude corrdinate of the bounding box
        south_latitude (float): The southern latitude corrdinate of the bounding box
        east_longitude (float): The eastern longitude corrdinate of the bounding box
        north_latitude (float): The northern latitude corrdinate of the bounding box

    Returns:
        A list with attractions. See Attraction for more details.

    Example:
        from tellme.B_get_location.location import get_bounding_box
        from tellme.C_get_attractions_nearby.get_attractions import get_nearby_attractions
        # 1km bounding box around Alexanderplatz
        bounding_box = get_bounding_box(52.521992, 13.413244, 1.0)
        get_nearby_attractions(west_longitude = bounding_box.bounds[0],
                               south_latitude = bounding_box.bounds[1],
                               east_longitude = bounding_box.bounds[2],
                               north_latitude = bounding_box.bounds[3])
    """
    # Initialize Overpass API
    api = overpy.Overpass()

    # Define an Overpass query for tourist attractions in a bounding box
    # The bounding boxes are defined as:
    # https://dev.overpass-api.de/overpass-doc/en/full_data/bbox.html
    # (latitude of the southern edge,
    #  longitude of the western edge,
    #  latitude of the norther edge,
    #  longitude of the eastern edge).
    query = f"""
    [out:json];
    node
    ["wikipedia"]
    ({south_latitude}, {west_longitude}, {north_latitude}, {east_longitude});  // Bounding box
    out;
    """

    # Get the attractions
    attractions = nodes_to_attractions(api.query(query).nodes)

    return attractions


def nodes_to_attractions(overpy_nodes: overpy.Result) -> list[Attraction]:
    """Extract the attraction information from overpy.Result nodes.

    Args:
        overpy_nodes (overpy.Result): Nodes with attraction data retrieved via overpy.

    Returns:
        list[Attraction]: A list of attractions. See Attraction for more details
    """
    attractions: list[Attraction] = []

    for node in overpy_nodes:
        name = node.tags.get('name', 'noname')
        location = {'latitude': float(node.lat), 'longitude': float(node.lon)}
        wikipedia_name = node.tags.get('wikipedia', 'noarticle')
        if (name == 'noname') | (wikipedia_name == 'noarticle'):
            next
        attractions.append(
            Attraction(
                name=name,
                location=location,
                wikipedia_link=f'https://wikipedia.org/wiki/{wikipedia_name}',
                wikidata_id=node.tags.get('wikidata'),
            )
        )
    return attractions
