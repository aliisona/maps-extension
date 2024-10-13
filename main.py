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

    # get safety score for each route and convert it to a string label
    safety_scores = [0.94, 0.12, 0.33] # mock for now while BE is done 
    safety_labels = convertScoresToString(safety_scores)

    return jsonify(safety_labels)

def convertScoresToString(safety_scores):
    safety_labels = []

    for score in safety_scores:
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