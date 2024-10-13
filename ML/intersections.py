import requests
import pandas as pd
import json
import statistics
from collections import defaultdict
from decimal import Decimal
from pyproj import Transformer
try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

amountCrashes = {1: 11626, 2: 2701, 3: 1168, 4: 681, 5: 373, 6: 290, 7: 206, 8: 156, 9: 122, 10: 82,
                  11: 99, 12: 60, 13: 66, 14: 48, 15: 28, 16: 42, 17: 36, 18: 26, 19: 39, 20: 19,
                  21: 18, 22: 17, 23: 14, 24: 21, 25: 28, 26: 16, 27: 9, 28: 10, 29: 5, 30: 8, 31: 7,
                  32: 10, 33: 7, 34: 8, 35: 5, 36: 8, 37: 9, 38: 5, 39: 9, 40: 8, 41: 5, 42: 3, 43: 7,
                  44: 3, 45: 4, 46: 3, 47: 4, 48: 5, 49: 2, 50: 6, 51: 2, 52: 1, 53: 1, 55: 2, 56: 1,
                  58: 1, 59: 1, 60: 4, 61: 1, 62: 1, 64: 2, 65: 6, 66: 2, 67: 1, 69: 3, 70: 4, 71: 2,
                  72: 3, 73: 1, 74: 3, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 82: 1, 83: 1, 84: 1, 86: 1,
                  87: 1, 88: 1, 90: 2, 91: 1, 92: 2, 94: 3, 96: 1, 97: 1, 98: 1, 100: 1, 102: 4, 108: 1,
                  110: 1, 113: 1, 116: 1, 122: 2, 127: 2, 128: 1, 131: 1, 133: 1, 135: 1, 141: 1, 148: 1,
                  156: 4, 166: 1, 185: 1, 225: 1, 226: 1, 236: 1, 324: 1, 334: 1, 350: 1, 368: 1, 396: 1,
                  398: 1, 439: 1, 486: 1, 566: 1, 595: 1, 630: 1, 667: 1, 716: 1, 1154: 1}

def convertXYtoLL(x: int, y: int) -> tuple[int, int]:
    transformer = Transformer.from_crs("EPSG:26986", "EPSG:4326", always_xy=True)
    out = transformer.transform(x, y)[::-1]

    lat = float(round(Decimal(out[0]), 4))
    lon = float(round(Decimal(out[1]), 4))
    return lat, lon

def extract_intersections(osm_xml: str, verbose=True) -> list[str]:
    root = ET.fromstring(osm_xml)

    counter = defaultdict(int)
    node_coords = {}

    for child in root:
        if child.tag == 'way':
            for item in child:
                if item.tag == 'nd':
                    counter[item.attrib['ref']] += 1

        elif child.tag == 'node':  
            node_id = child.attrib['id']
            if 'lat' in child.attrib and 'lon' in child.attrib:
                lat = float(round(Decimal(child.attrib['lat']), 4))
                lon = float(round(Decimal(child.attrib['lon']), 4))
                node_coords[node_id] = f"{lat},{lon}"

    intersection_coordinates = [
        node_coords[node_id]
        for node_id, count in counter.items()
        if count > 1 and node_id in node_coords
    ]

    return intersection_coordinates

def get_osm_data(south: int, west: int, north: int, east: int) -> str:
    url = f"https://overpass-api.de/api/interpreter?data=[out:xml];(node({south},{west},{north},{east});way({south},{west},{north},{east});rel({south},{west},{north},{east}););out body;"
    
    headers = {'Accept-Encoding': 'gzip'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None

def csv_to_json_pandas(csv_file, json_file):
    df = pd.read_csv(csv_file)

    location_data = {}
    for _, row in df.iterrows():
        latlon = convertXYtoLL(row['X_Cooordinate'], row['Y_Cooordinate'])

        if latlon:
            key = f"{latlon[0]},{latlon[1]}"
            crash_details = [
                row['Crash_Number'], row['Crash_Severity'], row['Maximum_Injury_Severity_Reported'],
                row['Number_of_Vehicles'], row['Total_Nonfatal_Injuries'], row['Total_Fatal_Injuries'],
                row['Weather_Condition']
            ]

            if key not in location_data:
                location_data[key] = [0]
                
            location_data[key][0] += 1
            location_data[key].append(crash_details)


    with open(json_file, 'w') as f:
        json.dump(location_data, f, indent=4)

def getCrashIndex(listCoords: list[dict[int, int]]) -> list[str]:
    crashOut = [0]
    for i in range(len(listCoords) - 1):
        lat1, long1 = listCoords[i][0], listCoords[i][1]
        lat2, long2 = listCoords[i + 1][0], listCoords[i + 1][1]
        out = []
        safetyScoreOut = []

        south, west, north, east = min(lat1, lat2), min(long1, long2), max(lat1, lat2), max(long1, long2)
        osmData = get_osm_data(south, west, north, east)
        intersectionList = extract_intersections(osmData)

        with open(json_file, 'r') as f:
            data = json.load(f)
            crashesLatLong = set(data.keys())
            common_intersections = set(intersectionList) & crashesLatLong

            for latLong in common_intersections:
                out.append(latLong)

            for x in out:
                safety_score = calculate_safety_score(data[x])
                if safety_score != 0:
                    safetyScoreOut.append(calculate_safety_score(data[x]))

        if len(safetyScoreOut) == 0:
            continue
        else:
            crashOut.append(statistics.mean(safetyScoreOut))
    
    return crashOut

def calculate_safety_score(crash_data: dict) -> float:
    total_crash_weight = 0
    total_crashes = 0
    
    severity_weights = {
        "Fatal injury (K)": 1.0,
        "Fatal": 1.0,
        "Serious injury": 0.8,
        "Suspected Serious Injury (A)": 0.7,
        "Non-fatal injury - Incapacitating": 0.6,
        "Non-fatal injury - Non-incapacitating": 0.4,
        "Suspected Minor Injury (B)": 0.3,
        "Possible injury (C)": 0.3,
        "No injury": 0.2,
        "No Apparent Injury (O)": 0.2,
        "Not reported": 0.1,
        "Property damage only": 0.05
    }
    
    mean_crashes = statistics.mean(amountCrashes.values())
    median_crashes = statistics.median(amountCrashes.values())

    num_crashes = crash_data[0]
    total_crashes += num_crashes

    return map_int_to_skewed_range(num_crashes)

def map_int_to_skewed_range(n: int) -> float:
    if 1 <= n <= 2:
        # Skew toward the lower end of 0-0.25
        return 0.25 * (n - 1) / 1  # n = 1 -> 0, n = 2 -> 0.25
    elif 3 <= n <= 5:
        # Skew toward 0.5 within 0.25-0.5
        return 0.25 + 0.25 * (n - 3) / 2  # n = 3 -> 0.25, n = 5 -> 0.5
    elif 6 <= n <= 9:
        # Skew toward 0.75 within 0.5-0.75
        return 0.5 + 0.25 * (n - 6) / 3  # n = 6 -> 0.5, n = 9 -> 0.75
    elif n >= 10:
        # Skew toward higher numbers within 0.75-1
        max_n = 1154  # Define the maximum value for scaling
        return 0.75 + 0.25 * (n - 10) / (max_n - 10)  # n = 10 -> 0.75, n = 1154 -> 1
    else:
        raise ValueError("Input must be between 1 and 1154")

csv_file = 'data/BostonCrashDetails.csv'
json_file = 'data/BostonCrashDetailsJson.json'

def safetyIndex(listCoords: list[str]) ->int:
    crashesInProximity = getCrashIndex(listCoords)

    return statistics.mean(crashesInProximity)

