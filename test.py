import requests
from datetime import datetime

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
