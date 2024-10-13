#imports
import requests
# from dotenv import load_dotenv
import os
#note: need function from intersections.py
import random
import math 
from function import findcrashdata()



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





