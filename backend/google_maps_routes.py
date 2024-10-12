from flask import Flask

app = Flask(__name__)

@app.route("/getstepscoordinates")
def getStepsCoordinates():
    return "";