from flask import Flask, request, jsonify
import googlemaps
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# init Google Maps client
gmaps = googlemaps.Client(key="AIzaSyAaLjlgAZSho352xp9K8oJLt-d7ARm_iHE")

@app.route('/get-walking-path', methods=['POST'])
def get_walking_path():
    data = request.json
    start = data.get('start')
    end = data.get('end')

    if not start or not end:
        return jsonify({'error': 'Start and end locations are required!'}), 400

    # fetch
    directions_result = gmaps.directions(start, end, mode="walking")

    if not directions_result:
        return jsonify({'error': 'No directions found'}), 404

    # extract paths
    route = directions_result[0]['legs'][0]
    duration = route['duration']['text']
    steps = [{'distance': step['distance']['text'], 'instruction': step['html_instructions']} for step in route['steps']]

    return jsonify({'duration': duration, 'steps': steps})

if __name__ == '__main__':
    app.run(debug=True)