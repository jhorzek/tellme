from geopy.distance import distance
from shapely.geometry import box

def get_bounding_box(lat, lon, dist_km):
    # Move north/south for lat bounds
    north = distance(kilometers=dist_km).destination((lat, lon), bearing=0)
    south = distance(kilometers=dist_km).destination((lat, lon), bearing=180)
    # Move east/west for lon bounds
    east = distance(kilometers=dist_km).destination((lat, lon), bearing=90)
    west = distance(kilometers=dist_km).destination((lat, lon), bearing=270)

    # Create bounding box using shapely
    return box(west.longitude, south.latitude, east.longitude, north.latitude)

bbox = get_bounding_box(latitude, longitude, box_size)
print(bbox.bounds)