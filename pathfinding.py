import json
import math

# Adrian is not cool
# Bet you'll never guess who wrote this
# L Ratio
# Hamdan Sheikh's License (states that anyone but Adrian Klos may use this in their project)
# (nobody is using this crappy code in their project)

# ChatGPT added this haversine function (gets the earths curvature and stuff)
def haversine(coord1, coord2):
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Earth radius in km
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

# --- Load GeoJSON ---
with open("filtered.geojson", "r") as f:
    data = json.load(f)

coords = [] 
graph = {}   

def add_edge(i, j):
    """Add undirected edge with haversine distance"""
    d = haversine(coords[i], coords[j])
    graph.setdefault(i, {})[j] = d
    graph.setdefault(j, {})[i] = d

for feature in data["features"]:
    geom = feature["geometry"]

    if geom["type"] == "Point":
        c = tuple(geom["coordinates"])
        if c not in coords:
            coords.append(c)

    elif geom["type"] == "LineString":
        indices = []
        for c in geom["coordinates"]:
            c = tuple(c)
            if c not in coords:
                coords.append(c)
            indices.append(coords.index(c))
        # connect consecutive nodes
        for i in range(len(indices)-1):
            add_edge(indices[i], indices[i+1])

# --- Find closest pair ---
# W3schools was pretty helpful for dikstras algorithm + AI
min_dist = float("inf")
closest_pair = None

for i in graph:
    for j, dist in graph[i].items():
        if dist < min_dist:
            min_dist = dist
            closest_pair = (i, j)

# --- Results ---
print("Total points loaded:", len(coords))
print(f"Closest points are {closest_pair[0]} and {closest_pair[1]}")
print(f"Distance between them: {min_dist*1000:.2f} meters")
print("Coordinates:")
print(f"  Point {closest_pair[0]}: {coords[closest_pair[0]]}")
print(f"  Point {closest_pair[1]}: {coords[closest_pair[1]]}")