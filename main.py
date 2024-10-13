from flask import Flask, jsonify, request
import requests
from flask import Flask, jsonify, request
import googlemaps
from dotenv import load_dotenv
import os
import random
from ML.intersections import *
from data import *
from ML.crime_level import *

load_dotenv()
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

def getStepsCoordinates(origin, destination, mode):
    if not origin or not destination or not mode:
        return jsonify({"error": "Missing required parameters: origin, destination, or mode"}), 400

    directions_result = gmaps.directions(origin, destination, mode=mode, alternatives=True)

    # For each route, get the list of coordinates representing key steps 
    routes = []
    # print(directions_result)
    for route in directions_result:
        route_coordinates = []

        for leg in route['legs']:
            for step in leg['steps']:
                latitude = step['start_location']['lat']
                longitude = step['start_location']['lng']
                
                # route_coordinates.append({
                #     "longitude": longitude,
                #     "latitude": latitude
                # })
                route_coordinates.append([latitude, longitude])
        # print("route coords", route_coordinates)
        routes.append(route_coordinates)
    # print("routes!", routes)
    return routes

@app.route("/getsafetyroutes", methods=['POST'])
def getSafetyRoutes():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    mode = data.get('mode') # "driving" or "walking"

    # params = {
    #     "origin": origin,
    #     "destination": destination,
    #     "mode": mode
    # }

    # get list of coordinates for each route
    routes = getStepsCoordinates(origin, destination, mode)
    # print("routes: ", routes)

    # for route in (routes):
    #     route_list.append(route)
    # return routes

    # print(routes)

    # get safety score for each route and convert it to a string label
    # safety_scores = [0.94, 0.12, 0.33] # mock for now while BE is done 
    safety_scores = safety_calculation(routes, mode)
    safety_labels = convertScoresToString(safety_scores)

    return jsonify(safety_labels)

def combine_coords(coords, threshold=0.01):
    combined = []

    i = 0
    while i < len(coords[:-1]):
        lat1, lon1 = coords[i][0], coords[i][1]
        lat2, lon2 = coords[i + 1][0], coords[i + 1][1]

        if abs(coords[i][0] - coords[i + 1][0]) < 0.01 or abs(coords[i][1] - coords[i + 1][1]) < 0.01:
            combined.append([lat2,lon2])
            i += 1
        else:
            combined.append([lat1,lat2])
        i += 1

    return combined

def safety_calculation(routes, mode):
    safety_score = 0
    weather_output = get_weather()
    routes_safety = []
    max_safety = 0
    min_safety = 0

    if mode == 'DRIVING':
        for i in range(len(routes)):
            current_routes_safety = safetyIndex(combine_coords(routes[i]))
            # print("current_route_safety: ", current_routes_safety)
            for j in range(len(routes[i])):
                safety_score += 3.5 * current_routes_safety
                begin_lat, begin_lon = routes[i][0]
                end_lat, end_lon = routes[i][-1]
                begin_zip = get_zipcode_from_coordinates(begin_lat, begin_lon)
                end_zip = get_zipcode_from_coordinates(end_lat, end_lon)
                safety_score = 0.1 * crime_stats(begin_zip) + 0.1 * crime_stats(end_zip)
            safety_score += 0.25 * weather_output
            routes_safety.append(safety_score)


    else:
        for i in range(len(routes)):
            current_routes_safety = safetyIndex(combine_coords(routes[i]))
            print("current_route_safety: ", current_routes_safety)
            for j in range(len(routes[i])):
                safety_score += 1.5 * current_routes_safety
                begin_lat, begin_lon = routes[i][0]
                end_lat, end_lon = routes[i][-1]
                begin_zip = get_zipcode_from_coordinates(begin_lat, begin_lon)
                end_zip = get_zipcode_from_coordinates(end_lat, end_lon)
                # print(crime_stats(end_zip))
                safety_score = 2 * crime_stats(begin_zip) + 3.5 * crime_stats(end_zip)
            safety_score += 3 * weather_output
            # print("safety score: ", safety_score)
            routes_safety.append(safety_score)

    max_safety = max(routes_safety)
    min_safety = min(routes_safety)

    for i in range(len(routes_safety)):
        if max_safety - min_safety != 0:
            routes_safety[i] = (routes_safety[i] - min_safety) / (max_safety - min_safety)
        else:
            routes_safety[i] = 0.0


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
            safety_labels.append("Low Risk")
        elif score <= .75:
            safety_labels.append("Moderate Risk")
        else:
            safety_labels.append("High Risk")

    return safety_labels

if __name__ == '__main__':
    app.run(debug=True)
