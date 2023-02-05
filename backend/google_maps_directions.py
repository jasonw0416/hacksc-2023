# import googlemaps
# from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import json
import urllib.parse

#
load_dotenv()
gmaps_key = os.getenv('GOOGLE_MAPS_API_KEY')
#
# gmaps = googlemaps.Client(key=gmaps_key)
#
# # Geocoding an address
# # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
# # Look up an address with reverse geocoding
# # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
#
# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now,
#                                      transit_mode="bus")
#
# # Validate an address with address validation
# # addressvalidation_result = gmaps.addressvalidation(['1600 Amphitheatre Pk'],
# #                                                     regionCode='US',
# #                                                     locality='Mountain View',
# #                                                     enableUspsCass=True)
#
# print(directions_result)

file = open('directions_output.html', 'w')

source_loc = "3734 Meadow Spring Drive, Sugar Land, Texas"
dest_loc = "First Colony Mall, Southwest Freeway, Sugar Land, TX"

source_loc_encoded = urllib.parse.quote(source_loc)
dest_loc_encoded = urllib.parse.quote(dest_loc)

url = "https://maps.googleapis.com/maps/api/directions/json?" \
      "origin=" + source_loc_encoded + \
      "&destination=" + dest_loc_encoded + \
      "&mode" \
      "=driving&key=" + gmaps_key

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

output = json.loads(response.text)

directions = []
num_directions = len(output["routes"][0]["legs"][0]["steps"])
for x in range(num_directions):
    directions.append(output["routes"][0]["legs"][0]["steps"][x]["html_instructions"])

print(directions)
print("Your distance is:", output["routes"][0]["legs"][0]["distance"]["text"])
print("Your trip will take:", output["routes"][0]["legs"][0]["duration"]["text"])

for y in range(len(directions)):
    file.write(directions[y] + '<br>')

file.close()
