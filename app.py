import requests
import json
import os
from datetime import datetime, timezone
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter


def get_closest_plane():

    API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
    r = requests.get(f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_icao=EGLC").json()

    flight_info = []

    now = datetime.now(timezone.utc)
    closest_guess = 100000000

    for flight in r['data']:
        est_arrival = datetime.fromisoformat(flight['arrival']['estimated'])

        arrival_delta = abs((now - est_arrival).seconds)
        if arrival_delta < closest_guess:
            closest_guess = arrival_delta
            closest_arrival = est_arrival
            departure_airport = flight['departure']['airport']

    return f"best guess of your flight is {departure_airport} which arrives at {closest_arrival.strftime('%H:%M')}"

print(get_closest_plane())

app = Flask(__name__)
skill_builder = SkillBuilder()
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.5376510e-fb7b-47b1-abaf-23077363a2cd", app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()