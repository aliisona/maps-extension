from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/getsafetyroutes", methods=['POST'])
def getSafetyRoutes():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    mode = request.args.get('mode') # "driving" or "walking"

    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode
    }

    # get list of coordinates for each route
    routes = requests.get("http://127.0.0.1:5000/getstepscoordinates", params=params)

    # get safety score for each route
    safety_scores = [0.94, 0.12, 0.33] # mock for now while BE is done 

    return jsonify(safety_scores)

if __name__ == '__main__':
    app.run(debug=True)