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

################
## PARAMETERS ##
################
# origin_loc = "3734 Meadow Spring Drive, Sugar Land, Texas"
# dest_loc = "First Colony Mall, Southwest Freeway, Sugar Land, TX"
# transportation_mode = "walking"
def find_directions(origin_loc, dest_loc, transportation_mode):
    try:

        ##############
        ## ENCODING ##
        ##############
        text_direction_steps = []
        text_direction_durations = []
        text_direction_distances = []

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

        #############
        ## PARSING ##
        #############
        output = json.loads(response.text)

        response_status = output["status"]  # NOT_FOUND or OK
        if response_status == "NOT_FOUND":
            print("One or more of the locations entered are incorrect. ")
            print("Try being more general / specific with your locations and make sure the names are entered correctly! ")

            dict = {
                "status": "LOCATION_NOT_FOUND"
            }

            json_object = json.dumps(dict)

            return json_object

        num_direction_steps = len(output["routes"][0]["legs"][0]["steps"])  # num of total directions
        # ^^ IndexError: list index out of range if theres an error!

        total_distance = output["routes"][0]["legs"][0]["distance"]["text"]
        total_duration = output["routes"][0]["legs"][0]["duration"]["text"]

        for direction_step in range(num_direction_steps):  # recording information about each direction step
            text_direction_steps.append(output["routes"][0]["legs"][0]["steps"][direction_step]["html_instructions"])
            text_direction_durations.append(output["routes"][0]["legs"][0]["steps"][direction_step]["duration"]["text"])
            text_direction_distances.append(output["routes"][0]["legs"][0]["steps"][direction_step]["distance"]["text"])

        #################
        ## File Output ##
        #################

        for text_direction_idx in range(len(text_direction_steps)):
            text_direction_steps[text_direction_idx] = text_direction_steps[text_direction_idx].replace("<b>", "")
            text_direction_steps[text_direction_idx] = text_direction_steps[text_direction_idx].replace("</b>", "")
            text_direction_steps[text_direction_idx] = text_direction_steps[text_direction_idx].replace("<div style=\"font-size:0.9em\">", ". ")
            text_direction_steps[text_direction_idx] = text_direction_steps[text_direction_idx].replace("</div>", "")
            text_direction_steps[text_direction_idx] = text_direction_steps[text_direction_idx].replace("<wbr/>", "")


        #################
        ## JSON Object ##
        #################
        dict = {}

        dict["status"] = "SUCCESS"
        dict["start"] = origin_loc
        dict["dest"] = dest_loc
        dict["mode"] = transportation_mode
        dict["t_dist"] = total_distance
        dict["t_time"] = total_duration

        dict["steps"] = []
        for text_direction_idx in range(len(text_direction_steps)):
            step = {}
            step["d"] = text_direction_distances[text_direction_idx]
            step["v"] = text_direction_steps[text_direction_idx]
            dict["steps"].append(step)

        json_object = json.dumps(dict)

        if len(json_object) >= 1520:
            overflow = {
                "status" : "CHARACTER_EXCEEDED"
            }
            json_object = json.dumps(overflow)
            print(json_object)
            return json_object

        print(json_object)

        return json_object
    except:
        exception = {
            "status": "MAP_EXCEPTION"
        }
        json_object = json.dumps(exception)
        print(json_object)
        return json_object



# find_directions("7 Tufts Ct, NJ","USC","transit")

# total distance
# total duration

# for each step of the project
# distance
# duration
# html_instructions (TEXT)
# travel_mode
