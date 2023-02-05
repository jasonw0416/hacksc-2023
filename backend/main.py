from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>TEST</h1>"


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    body = request.form.get('Body')

    if body == "HELLO":
        resp.message("WHYYYY???")
    else:
        resp.message("WOW")

    # Add a message
    # resp.message("HI!")

    return str(resp)


if __name__ == "__main__":
    load_dotenv()
    gmaps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    app.run(debug=True)

