from flask import Flask, jsonify, request
import requests
import googlemaps
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

@app.route("/getsafetyroutes", methods=['POST'])
def getSafetyRoutes():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    mode = request.args.get('mode') # "driving" or "walking"

    # params = {
    #     "origin": origin,
    #     "destination": destination,
    #     "mode": mode
    # }

    # get list of coordinates for each route
    routes = getStepsCoordinates(origin, destination, mode)
    print(routes)
    safety_routes_calc = safety_calculation(routes, mode)

    # # get safety score for each route and convert it to a string label
    # safety_scores = [0.94, 0.12, 0.33] # mock for now while BE is done 
    safety_labels = convertScoresToString(safety_routes_calc)

    return jsonify(safety_labels)

# other functions
def getStepsCoordinates(origin, destination, mode):
    # origin = request.args.get('origin')
    # destination = request.args.get('destination')
    # mode = request.args.get('mode') # "driving" or "walking"

    if not origin or not destination or not mode:
        print("error, missing things!")
        return ({"error": "Missing required parameters: origin, destination, or mode"}), 400

    directions_result = gmaps.directions(origin, destination, mode)
    print(directions_result)

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


def safety_calculation(routes, mode):
    weatheroutput = get_weather_description_boston()
    crashdata = get_crash_data()

    safety_score = 0
    routes_safety = []
    print(routes)
    print("testing")

    if mode == 'DRIVING':
        for i in range(len(routes)):
            print(routes[i])
            for b in range(len(routes[i])): #for each coordinate pair in route
                
                safety_score += 3.5 * 1
        safety_score += 0.25 * weatheroutput
        routes_safety.append(safety_score) #append the total safety score for this route

    else:
        for i in range(len(routes)):
            for b in range(len(routes[i])):
                safety_score += 1
        safety_score += 3 * weatheroutput
        routes_safety.append(safety_score)

    max = routes_safety.max()
    min = routes_safety.min()

    for i in routes_safety:
        routes_safety[i] = (routes_safety[i] - min)/(max - min)

    return routes_safety

def get_crash_data():
    crash_data = 1

    return 1
def get_weather_description_boston():
    api_key = os.getenv('OPENWEATHER_API_KEY')

    zip_code = "02108"  # boston
    country_code = "US"  
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'zip': f'{zip_code},{country_code}',
        'appid': api_key,
        'units': 'metric'  
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        # print(f"Today's weather in Boston, MA: {weather_desc}")
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
        print(score)
        if score <= 0.25:
            safety_labels.append("High Risk")
        elif score <= 0.5:
            safety_labels.append("Moderate Risk")
        elif score <= 0.75:
            safety_labels.append("Low Risk")
        else:
            safety_labels.append("Safe")

    return safety_labels

if __name__ == '__main__':
    app.run(debug=True)