from tellme import create_podcast

audio = create_podcast.create_podcast(
    ['https://de.wikipedia.org/wiki/Nikolaikirche_(Berlin)']
)

import overpy

# Initialize Overpass API
api = overpy.Overpass()

# Define an Overpass query for tourist attractions in a bounding box
query = """
[out:json];
node
  ["tourism"="attraction"]
  (52.5, 13.3, 52.6, 13.4);  // Bounding box around Berlin, Germany
out;
"""

# Run the query
result = api.query(query)

# Print the results
for node in result.nodes:
    print(
        f'Attraction: {node.tags.get("name", "Unnamed")} - Lat: {node.lat}, Lon: {node.lon}'
    )
