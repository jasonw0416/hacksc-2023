import os
from dotenv import load_dotenv

import requests

import json
import urllib.parse

####################
## INITIALIZATION ##
####################
load_dotenv()
gmaps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
file = open('directions_output.html', 'w')
text_directions = []
text_direction_steps = []
text_direction_durations = []
text_direction_distances = []

################
## PARAMETERS ##
################
origin_loc = "3734 Meadow Spring Drive, Sugar Land, Texas"
dest_loc = "First Colony Mall, Southwest Freeway, Sugar Land, TX"
transportation_mode = "walking"

##############
## ENCODING ##
##############
origin_loc_encoded = urllib.parse.quote(origin_loc)
dest_loc_encoded = urllib.parse.quote(dest_loc)
transportation_mode_encoded = urllib.parse.quote(transportation_mode)

# limited to 8192 characters
maps_req_url = "https://maps.googleapis.com/maps/api/directions/json?" \
               "origin=" + origin_loc_encoded + \
               "&destination=" + dest_loc_encoded + \
               "&mode=" + transportation_mode_encoded + \
               "&key=" + gmaps_api_key

# # # https://developers.google.com/maps/documentation/directions/get-directions
# avoid avoid=tolls|highways|ferries.
# departure_time
# language ~> https://developers.google.com/maps/faq#languagesupport
# mode=driving|walking|bicycling|transit
# transit_mode=bus|subway|train|tram|rail
# units=metric|imperial

payload = {}
headers = {}

#############
## REQUEST ##
#############
response = requests.request("GET", maps_req_url, headers=headers, data=payload)
# print(response.text)

#############
## PARSING ##
#############
output = json.loads(response.text)
num_direction_steps = len(output["routes"][0]["legs"][0]["steps"]) # num of total directions
travel_mode = output["routes"][0]["legs"][0]["steps"][0]["travel_mode"]
total_distance = output["routes"][0]["legs"][0]["distance"]["text"]
total_duration = output["routes"][0]["legs"][0]["duration"]["text"]

for direction_step in range(num_direction_steps): # recording information about each direction step
    text_direction_steps.append(output["routes"][0]["legs"][0]["steps"][direction_step]["html_instructions"])
    text_direction_durations.append(output["routes"][0]["legs"][0]["steps"][direction_step]["duration"]["text"])
    text_direction_distances.append(output["routes"][0]["legs"][0]["steps"][direction_step]["distance"]["text"])

#################
## File Output ##
#################
file.write('<h1>' + "Travel Directions" + '</h1>')
file.write('<small><em>' + "Traveling by: " + travel_mode + '<em></small>')
file.write('<h4><em>' + "Total Trip Distance: " + total_distance + '<em></h4>')
file.write('<h4><em>' + "Total Trip Duration: " + total_duration + '<em></h4>')

for text_direction_idx in range(len(text_direction_steps)):
    file.write('<p>'
               + str(text_direction_idx + 1) + ". "
               + "<" + text_direction_distances[text_direction_idx] + "> "
               + text_direction_steps[text_direction_idx]
               + " ~ " + text_direction_durations[text_direction_idx]
               + '<p>')

file.close()

# total distance
# total duration

# for each step of the project
# distance
# duration
# html_instructions (TEXT)
# travel_mode