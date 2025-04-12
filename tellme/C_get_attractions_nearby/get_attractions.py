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
    ["tourism"="attraction"]
    ({south_latitude}, {west_longitude}, {north_latitude}, {east_longitude});  // Bounding box around Berlin, Germany
    out;
    """

    # Get the attractions
    attractions = api.query(query)

    return attractions
