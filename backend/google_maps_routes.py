from flask import Flask, jsonify, request
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

@app.route("/getstepscoordinates")
def getStepsCoordinates():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    mode = request.args.get('mode') # "driving" or "walking"

    # origin = "MIT, 77 Massachusetts Ave, Cambridge, MA 02139"
    # destination = "Harvard Square, Cambridge, MA 02138"

    if not origin or not destination or not mode:
        return jsonify({"error": "Missing required parameters: origin, destination, or mode"}), 400

    # Get directions
    directions_result = gmaps.directions(origin, destination, mode=mode)

    # Print the response (for demonstration)
    print(directions_result)

    return "called";

if __name__ == '__main__':
    app.run(debug=True)