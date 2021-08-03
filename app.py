import requests
import json
import os
from datetime import datetime, timezone
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy import distance
from flask import Flask
from flask_ask import Ask, statement


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
            airline_name = flight['airline']['name']

    return f"best guess of your flight is the {airline_name} flight from {departure_airport} which arrives into London City at {closest_arrival.strftime('%H:%M')}"

def get_iss_distance():
    resp = requests.get("http://api.open-notify.org/iss-now.json").json()

    iss_geolocator = Nominatim(user_agent="ISS")
    iss_location = iss_geolocator.reverse(f"{resp['iss_position']['latitude']}, {resp['iss_position']['longitude']}")


    home_geolocator = Nominatim(user_agent="HOME")
    home_location = home_geolocator.geocode("1 Tidal Basin Road London")

    dist = distance.geodesic(iss_location.point, home_location.point).miles
    return dist


app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('PlaneInfo')
def plane_response():
    try:
        return statement(get_closest_plane())
    except:
        try:
            return statement('''
                <speak>
                    <amazon:emotion name="excited" intensity="medium">
                        I am very excited!
                    </amazon:emotion>
                    <amazon:emotion name="disappointed" intensity="high">
                        Now I am a sad alexa.
                    </amazon:emotion>
                </speak>''')
        except Exception as e:
            print(e)

@ask.intent('ISSInfo')
def iss_response():
    dist = get_iss_distance()
    if dist > 5000:
        return statement(f"The ISS is {dist} miles away! thats further than the moon")
    elif dist > 3000:
        return statement(f"The ISS is {dist} miles away! thats longer than a runner bean")
    else:
        return statement(f"The ISS is {dist} miles away! thats closer than a lambs whistle")

@ask.intent('AMAZON.StopIntent')
def stop_intent():
    return None

@ask.intent('AMAZON.HelpIntent')
def help_intent():
    return statement("The only help you're getting is ")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert/cert.pem', 'cert/key.pem'))
