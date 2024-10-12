from flask import Flask, jsonify, request
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

print(os.getenv('GOOGLE_MAPS_API_KEY'))
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

    return jsonify(routes)

if __name__ == '__main__':
    app.run(debug=True)