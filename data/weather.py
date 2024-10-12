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
    else:
        print(f"Error: Unable to fetch weather for Boston. Status code: {response.status_code}")

if __name__ == "__main__":
    get_weather_description_boston(key=os.getenv('OPENWEATHER_API_KEY'))