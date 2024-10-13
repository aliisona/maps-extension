from flask import Flask, jsonify, request
import requests
from flask import Flask, jsonify, request
import googlemaps
from dotenv import load_dotenv
import os
import random

load_dotenv()
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

@app.route("/getstepscoordinates")
def getStepsCoordinates():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    mode = request.args.get('mode') # "driving" or "walking"

    if not origin or not destination or not mode:
        return jsonify({"error": "Missing required parameters: origin, destination, or mode"}), 400

    directions_result = gmaps.directions(origin, destination, mode=mode)

    # For each route, get the list of coordinates representing key steps 
    routes = []
    for route in directions_result:
        route_coordinates = []

        for leg in route['legs']:
            for step in leg['steps']:
                latitude = step['start_location']['lat']
                longitude = step['start_location']['lng']
                
                route_coordinates.append({
                    "longitude": longitude,
                    "latitude": latitude
                })
        
        routes.append(route_coordinates)

    return routes

@app.route("/getsafetyroutes", methods=['POST'])
def getSafetyRoutes():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    mode = data.get('mode') # "driving" or "walking"

    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode
    }

    # get list of coordinates for each route
    route_list = []
    routes = requests.get("http://127.0.0.1:5000/getstepscoordinates", params=params)

    for route in (routes):
        route_list.append(route)
    # return routes

    # print(routes)

    # get safety score for each route and convert it to a string label
    # safety_scores = [0.94, 0.12, 0.33] # mock for now while BE is done 
    safety_scores = safety_calculation(route_list, mode)
    safety_labels = convertScoresToString(safety_scores)

    return jsonify(safety_labels)

def safety_calculation(routes, mode):
    safety_score = 0
    weather_output = get_weather()
    routes_safety = []
    max_safety = 0
    min_safety = 0

    if mode == 'DRIVING':
        for i in range(len(routes())):
            for b in range(len(routes[i])):
                safety_score += 3.5 * 1
        safety_score += 0.25 * weather_output
        routes_safety.append(safety_score)

    else:
        for i in range(len(routes)):
            for b in range(len(routes[i])):
                safety_score += random.uniform(50, 70)
        safety_score += 3 * weather_output
        routes_safety.append(safety_score)

    max_safety = max(routes_safety)
    min_safety = min(routes_safety)

    # for i in range(len(routes_safety)):
    #     if max_safety - min_safety != 0:
    #         routes_safety[i] = (routes_safety[i] - min_safety) / (max_safety - min_safety)
    #     else:
    #         routes_safety[i] = 0.0


    return routes_safety

def get_weather():
    zip_code = "02108"  # boston
    country_code = "US"  
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'zip': f'{zip_code},{country_code}',
        'appid': os.getenv('OPENWEATHER_API_KEY'),
        'units': 'metric'  
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        print(f"Today's weather in Boston, MA: {weather_desc}")
        match (weather_desc):
            case "clear sky":
                return 0
            case "few clouds":
                return 0.1
            case "scattered clouds":
                return 0.2
            case "broken clouds":
                return 0.3
            case "shower rain":
                return 0.5
            case "rain":
                return 0.6
            case "thunderstorm":
                return 0.9
            case "snow":
                return 0.7
            case "mist":
                return 0.4
            case _:
                return 0
            
    else:
        print(f"Error: Unable to fetch weather for Boston. Status code: {response.status_code}")

def convertScoresToString(safety_scores):
    safety_labels = []

    for score in safety_scores:
        if score <= .25:
            safety_labels.append("Safe")
        elif score <= .5:
            safety_labels.append("Moderate Risk")
        elif score <= .75:
            safety_labels.append("High Risk")
        else:
            safety_labels.append("DANGEROUS!!!")

    return safety_labels


if __name__ == '__main__':
    app.run(debug=True)