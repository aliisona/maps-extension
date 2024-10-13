import pandas as pd 
import numpy as np
import requests
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
def get_zipcode_from_coordinates(coordinates):
    latitude, longitude = coordinates
    geolocator = Nominatim(user_agent="my_agent")
    
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location.raw['address']
        
        # Check if 'postcode' is in the address dictionary
        if 'postcode' in address:
            return address['postcode']
        else:
            return "Zip code not found"
    
    except (GeocoderTimedOut, GeocoderServiceError):
        return "Error: Geocoding service timed out or encountered an error"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
def get_crime_data(zip_code):
    url = f'https://zylalabs.com/api/824/crime+data+by+zipcode+api/583/get+crime+rates+by+zip?zip={zip_code}'
    headers = {'Authorization': 'Bearer 5508|2OEbQwM32fjOdjq9EMKTh3clqFRLQUYO719qbhxp'}
    response = requests.get(url, headers=headers)
    return response.json()
def calculate_safety_score(crime_data):
    grade_values = {'A+': 1, 'A': 2, 'A-': 3, 'B+': 4, 'B': 5, 'B-': 6, 
                    'C+': 7, 'C': 8, 'C-': 9, 'D+': 10, 'D': 11, 'D-': 12, 'F': 13}
    
    overall_grade = crime_data['Overall']['Overall Crime Grade']
    violent_grade = crime_data['Overall']['Violent Crime Grade']
    property_grade = crime_data['Overall']['Property Crime Grade']
    other_grade = crime_data['Overall']['Other Crime Grade']
    
    overall_score = grade_values[overall_grade]
    violent_score = grade_values[violent_grade]
    property_score = grade_values[property_grade]
    other_score = grade_values[other_grade]
    
    safety_score = (overall_score + violent_score + property_score + other_score) / 4
    return safety_score / 13
