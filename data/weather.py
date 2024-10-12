import requests
from dotenv import load_dotenv
import os

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

