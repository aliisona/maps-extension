import requests
import pandas as pd
import json
from decimal import Decimal
from pyproj import Transformer
try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

def convertXYtoLL(x: int, y: int) -> tuple[int, int]:
    transformer = Transformer.from_crs("EPSG:26986", "EPSG:4326", always_xy=True)
    out = transformer.transform(x, y)[::-1]

    lat = float(round(Decimal(out[0]), 4))
    lon = float(round(Decimal(out[1]), 4))
    return lat, lon

def extract_intersections(osm_xml: str, verbose=True) -> list[tuple[float, float]]:
    root = ET.fromstring(osm_xml)
    
    counter = {}

    for child in root:
        if child.tag == 'way':
            for item in child:
                if item.tag == 'nd':
                    nd_ref = item.attrib['ref']
                    if nd_ref not in counter:
                        counter[nd_ref] = 0
                    counter[nd_ref] += 1

    intersections = list(filter(lambda x: counter[x] > 1, counter))
    intersection_coordinates = []

    for child in root:
        if child.tag == 'node' and child.attrib['id'] in intersections:
            if 'lat' in child.attrib and 'lon' in child.attrib:
                coordinate = (float(child.attrib['lat']), float(child.attrib['lon']))
                #DEBUG
                # if verbose:
                #     print(coordinate)
                intersection_coordinates.append(coordinate)

    return intersection_coordinates

# Boston example coordinates
# Southwest corner: (42.30, -71.10)
# Northeast corner: (42.40, -71.00)
def get_osm_data(south: int, west: int, north: int, east: int) -> str:
    url = f"https://overpass-api.de/api/interpreter?data=[out:xml];(node({south},{west},{north},{east});way({south},{west},{north},{east});rel({south},{west},{north},{east}););out body;"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None

# Example with Boston
# osm_data = get_osm_data(42.30, -71.10, 42.40, -71.00)

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

csv_file = 'data/BostonCrashDetails.csv'
json_file = 'data/BostonCrashDetailsJson.json'

