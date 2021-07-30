import requests
import json
import os
from datetime import datetime, timezone
from flask import Flask, render_template
from flask_ask import Ask, statement


# def get_closest_plane():

#     API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
#     r = requests.get(f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_icao=EGLC").json()

#     flight_info = []

#     now = datetime.now(timezone.utc)
#     closest_guess = 100000000

#     for flight in r['data']:
#         est_arrival = datetime.fromisoformat(flight['arrival']['estimated'])

#         arrival_delta = abs((now - est_arrival).seconds)
#         if arrival_delta < closest_guess:
#             closest_guess = arrival_delta
#             closest_arrival = est_arrival
#             departure_airport = flight['departure']['airport']

#     return f"best guess of your flight is {departure_airport} which arrives at {closest_arrival.strftime('%H:%M')}"

# print(get_closest_plane())


app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('PlaneInfo')
def plane_response():
    return statement("Unfortunately I do not have eyes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert/cert.pem', 'cert/key.pem'))
