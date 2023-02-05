from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
from dotenv import load_dotenv
from backend import google_maps_directions as gmap
import time

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>TEST</h1>"


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    try:
        # output = gmap.find_directions("USC", "UCLA", "driving")
        # if (len(output) >= 1600):
        #     for i in range ((len(output) // 1500+1)):
        #         if (1500*(i+1) >= len(output)):
        #             resp.message(output[1500*i:])
        #         else:
        #             resp.message(output[1500*i:1500*(i+1)])
        # else:
        #     resp.message(output)


        body = request.form.get('Body')
        maps = json.loads(body)

        start = maps['start']
        dest = maps['destination']
        mode = maps['mode']

        if not start or not dest or not mode:
            dict = {
                "status" : "EMPTY_INPUT"
            }

            json_object = "SOF " + json.dumps(dict) + " EOF"
            resp.message(json_object)
        else:
            output = gmap.find_directions(start, dest, mode)
            output = output.replace('\n', ' ').replace('\r', '') # replace useless chars

            if len(output) >= 1600:
                for i in range((len(output) // 1500 + 1)):
                    if 1500 * (i + 1) >= len(output):
                        resp.message(output[1500 * i:])
                    else:
                        resp.message(output[1500 * i:1500 * (i + 1)])
                    time.sleep(0.2)
            else:
                resp.message(output)

        return str(resp)

    except:
        dict = {
            "status": "MAIN_EXCEPTION"
        }

        json_object = "SOF " + json.dumps(dict) + " EOF"
        resp.message(json_object)

        return json_object


if __name__ == "__main__":
    load_dotenv()
    gmaps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    app.run(debug=True)



# JSON object will have:

"""
{
    "status": (string) "EMPTY_INPUT" / "SUCCESS" / "LOCATION_NOT_FOUND"
    "start": (string) "start location"
    "dest": (string) "destination"
    "mode": (string) "driving" / "walking" / "bicycling" / "transit"
    "total_dist" : (string) "total distination"
    "total_time" : (string) "total time duration"
    "steps" : (dict) {
        1: (dict) {
            "dist": (float) distance (e.g. 1.5 mi)
            "direction": (string) "direction information" (e.g. Walk to Kendall Park Roller Skating Rink)
            "time": (string) "time" (e.g. 12 hours 40 mins)
        }
        2: (dict) {...}
        3: (dict) {...}
        4: (dict) {...}
    }
}
"""