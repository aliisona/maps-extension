#imports
import requests
# from dotenv import load_dotenv
import os
#note: need function from intersections.py
import random
import math 
from function import findcrashdata()
from intersections import *
import json



def safety_calculation(routes, weatheroutput, crashdata, transportation_method):
    safety_score = 0
    routes_safety = []

    if transportation_method == 'car':
        for i in range(len(routes())):
            for b in range(len(routes[i])):
                safety_score += 3.5 * findcrashdata(routes[i][b])
        safety_score += 0.25 * weatheroutput
        routes_safety.append(safety_score)

    else:
        for i in range(len(routes)):
            for b in range(len(routes[i])):
                safety_score += findcrashdata(routes[i][b])
        safety_score += 3 * weatheroutput
        routes_safety.append(safety_score)

    max = routes_safety.max()
    min = routes_safety.min()

    for i in routes_safety:
        routes_safety[i] = (routes_safety[i] - min)/(max - min)

    return routes_safety


    


#Testing

def generate_random_coordinates(num_groups, num_coordinates):
    data = []
    for _ in range(num_groups):
        group = []
        for _ in range(num_coordinates):
            latitude = round(random.uniform(-90, 90), 7)
            longitude = round(random.uniform(-180, 180), 7)
            group.append({"latitude": latitude, "longitude": longitude})
        data.append(group)
    return data

# Generate random data
random_data = generate_random_coordinates(5, 5)  # 2 groups, each with 3 coordinates
print(random_data)










#INTERSECTIONS



#WEATHER STUFF
# Load environment variables from .env file
load_dotenv()

def get_weather_description_boston(api_key):
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

if __name__ == "__main__":
    api_key = os.getenv('OPENWEATHER_API_KEY')
    (get_weather_description_boston(api_key))




testData2 = [
    {
      "latitude": 42.28608897461656,
      "longitude": -71.09164191096448
    },
    {
      "latitude": 42.31287346648963,
      "longitude": -71.05243806098352
    },
    {
      "latitude": 42.37070952784675,
      "longitude": -71.11276140389808
    }
  ]

testData = [[42.2782195, -71.1599579], [42.2806449, -71.15801549999999], [42.2804387, -71.1575053], 
            [42.28287599999999, -71.1555606], [42.28295809999999, -71.1556179], [42.284184, -71.154533], 
            [42.284093, -71.1543338], [42.2849532, -71.1492689], [42.2855803, -71.14853219999999], 
            [42.2859344, -71.14885869999999], [42.2867813, -71.1310721], [42.2872433, -71.1295566], 
            [42.2871424, -71.127555], [42.2982719, -71.1158051], [42.2979542, -71.1150834], 
            [42.2999512, -71.11359790000002], [42.3284867, -71.0862111], [42.3296042, -71.0861338], 
            [42.3485676, -71.0654176], [42.3588916, -71.0598146], [42.3592295, -71.05951139999999], 
            [42.3596904, -71.0587764], [42.3614983, -71.0575155], [42.36161449999999, -71.0575255], 
            [42.3621363, -71.0566001], [42.3621985, -71.056697], [42.36293510000001, -71.05615879999999], 
            [42.3629781, -71.0562307]] 

sample_crash_data = [
        5,
        [
            2576250,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Cloudy/Cloudy"
        ],
        [
            2637363,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            2618951,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear"
        ],
        [
            3251865,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            3973651,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            3,
            0,
            "Clear"
        ]
    ]

sample_data_2 = [
        10,
        [
            2577005,
            "Unknown",
            "Not Applicable",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            3179577,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            3322001,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            1,
            1,
            0,
            "Clear"
        ],
        [
            3432921,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear"
        ],
        [
            3640531,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            2,
            0,
            "Cloudy"
        ],
        [
            4036756,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            4363739,
            "Not Reported",
            "Not Applicable",
            2,
            0,
            0,
            "Clear"
        ],
        [
            4376978,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            1,
            0,
            "Clear/Clear"
        ],
        [
            4433027,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            4724993,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear"
        ]
    ]

def safetyIndex(listCoords: list[str]) ->int:
    crashesInProximity = getCrashIndex(listCoords)

    return statistics.mean(crashesInProximity)
