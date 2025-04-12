import overpy


def get_nearby_attractions(
    west_longitude: float,
    south_latitude: float,
    east_longitude: float,
    north_latitude: float,
) -> overpy.Result:
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
    ["tourism"="attraction"]["wikipedia"]
    ({south_latitude}, {west_longitude}, {north_latitude}, {east_longitude});  // Bounding box around Berlin, Germany
    out;
    """

    # Get the attractions
    attractions = nodes_to_attractions(api.query(query).nodes)

    return attractions


class Attraction:
    name: str
    location: dict[str, float] = {'latitude': None, 'longitude': None}
    wikipedia_link: str

    def __init__(self, name: str, location: dict[str, float], wikipedia_link: str):
        self.name = name
        self.location = location
        self.wikipedia_link = wikipedia_link


def nodes_to_attractions(overpy_nodes: overpy.Result) -> list[Attraction]:
    attractions: list[Attraction] = []

    for node in overpy_nodes:
        name = node.tags.get('name', 'noname')
        location = {'latitude': float(node.lat), 'longitude': float(node.lon)}
        wikipedia_name = node.tags.get('wikipedia', 'noarticle')
        if (name == 'noname') | (wikipedia_name == 'noarticle'):
            next
        attractions.append(
            Attraction(
                name=name[0],
                location=location,
                wikipedia_link=f'https://wikipedia.org/wiki/{wikipedia_name}',
            )
        )
    return attractions
