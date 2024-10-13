import pandas as pd 
import numpy as np
import requests
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

grade_values = {'A+': 1, 'A': 2, 'A-': 3, 'B+': 4, 'B': 5, 'B-': 6, 
                'C+': 7, 'C': 8, 'C-': 9, 'D+': 10, 'D': 11, 'D-': 12, 'F': 13}

def get_zipcode_from_coordinates(x, y):
    geolocator = Nominatim(user_agent="my_agent")
    try:
        location = geolocator.reverse(f"{x}, {y}")
        address = location.raw['address']
        return address.get('postcode', "Zip code not found")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return f"Geocoding error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def crime_stats(zip_code):
    url = f'https://zylalabs.com/api/824/crime+data+by+zipcode+api/583/get+crime+rates+by+zip?zip={zip_code}'
    headers = {'Authorization': 'Bearer 5508|2OEbQwM32fjOdjq9EMKTh3clqFRLQUYO719qbhxp'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        crime_data = response.json()
        overall_grade = crime_data['Overall']['Overall Crime Grade']
        violent_grade = crime_data['Overall']['Violent Crime Grade']
        property_grade = crime_data['Overall']['Property Crime Grade']
        other_grade = crime_data['Overall']['Other Crime Grade']
        overall_score = grade_values.get(overall_grade, 0)
        violent_score = grade_values.get(violent_grade, 0)
        property_score = grade_values.get(property_grade, 0)
        other_score = grade_values.get(other_grade, 0)
        safety_score = (overall_score + violent_score + property_score + other_score) / 4
        return safety_score / 13
    else:
        return f"API error: {response.status_code} - {response.text}"
    

