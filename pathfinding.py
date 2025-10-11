import requests
import json
import math
from geopy.geocoders import Nominatim

# TODO: Get GPS system to track your current location
# I need help on implementing that. (i don't know where to start)
# I know you probably aren't even reading these damn comments, Adrian Clause

# userGoingtoAddressInput = input("Where would you like to go?")
API_KEY = "AIzaSyDLnGHw5jc227pi3LBqjtr74k3ybwwcWCM"
ADDRESS =  "Schaumburg Town Square, 200 S Roselle Rd, Schaumburg, IL 60193"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
coords = []
graph = {}
longitude = None
latitude = None 
formatted_address = None

# This piece is for the user's location (GPS)
# print("-" * 30)
# userCurrentAddressInput = input("Where are you right now?")
# geolocator = Nominatim(user_agent="PathfindingAlgo")
# location = geolocator.geocode(userCurrentAddressInput)
# print(location.address)
# print(location.longitude, location.latitude)
# usersCurrent_location_longitude = location.longitude
# usersCurrent_location_latitude = location.latitude
currentLocation = [-88.0536360957661, 42.0629908820274]

# --- Build the request dictionary ---
params = {
    "address": ADDRESS,
    "key": API_KEY
}

# --- Make the request and handle potential HTTP errors ---
try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: Could not decode JSON. Raw response text:")
        print(response.text)
        exit()

    if data['status'] == 'OK':
        # Get the first result (usually the most accurate)
        result = data['results'][0]

        # Extract info
        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']
        formatted_address = result['formatted_address']

        # Print the results
        print("-" * 30)
        print(f"Address: {formatted_address}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print("-" * 30)
        
        # --- Load GeoJSON ---
        with open("filtered.geojson", "r") as f:
            data = json.load(f)

        # --- Process features ---
        for feature in data["features"]:
            geom = feature["geometry"]

            if geom["type"] == "Point":
                c = tuple(geom["coordinates"])
                if c not in coords:
                    coords.append(c)
                    print("Points appended.")

            elif geom["type"] == "LineString":
                indices = []
                for c in geom["coordinates"]:
                    c = tuple(c)
                    if c not in coords:
                        coords.append(c)
                        coords.append(longitude)
                        coords.append(latitude)
                        # coords.append(usersCurrent_location_longitude)
                        # coords.append(usersCurrent_location_latitude)
                        print("Coordinates appended.")
                    indices.append(coords.index(c))

        # --- Find closest pair ---
        min_dist = float("inf")
        closest_pair = None

     # How close counts as "near" (in degrees, roughly)
    threshold = 0.01  # small number, about ~1 km

# Loop through all features 
    for feature in data["features"]:
            geometry = feature["geometry"]
    
    if geometry["type"] == "Point":
        point_lon, point_lat = geometry["coordinates"]
        
        # Simple distance check
        distance = ((point_lon - currentLocation[0])**2 + (point_lat - currentLocation[1])**2)**0.5
        
        if distance < threshold:
            print("Nearby point found:", feature)

        # if closest_pair:
        #     print(f"Closest destination to {currentLocation} is {closest_pair[1]} ({min_dist} km)")

        # if closest_pair:
        #     if coords[closest_pair[0]]: #== (longitude, latitude):
        #         print("-" * 30)
        #         print(f"Coordinates: {coords[closest_pair[0]]} \n route to: \n {coords[closest_pair[1]]}")
        #         print("-" * 30)
        #         print("\n Adrian, this algorithm is watching you.")
        #         print("\n Good luck implementing this lmao")
        #     else:
        #         print("No match found!")

    else:
        print(f"Geocoding failed. API Status: {data['status']}")
        if 'error_message' in data:
            print(f"Error Message: {data['error_message']}")

except requests.exceptions.RequestException as e:
    print(f"Network or HTTP error occurred: {e}")
