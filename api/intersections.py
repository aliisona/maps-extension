from pyproj import Transformer
import requests
try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

def convertXYtoLL(x, y):
    transformer = Transformer.from_crs("EPSG:26986", "EPSG:4326", always_xy=True)
    return transformer.transform(x, y)[::-1]

def extract_intersections(osm, verbose=True):
    tree = ET.parse(osm)
    root = tree.getroot()
    counter = {}
    for child in root:
        if child.tag == 'way':
            for item in child:
                if item.tag == 'nd':
                    nd_ref = item.attrib['ref']
                    if not nd_ref in counter:
                        counter[nd_ref] = 0
                    counter[nd_ref] += 1

    intersections = list(filter(lambda x: counter[x] > 1,  counter))
    intersection_coordinates = []

    for child in root:
        if child.tag == 'node' and child.attrib['id'] in intersections:
            coordinate = child.attrib['lat'] + ',' + child.attrib['lon']
            #DEBUG
            # if verbose:
            #     print(coordinate)
            intersection_coordinates.append(coordinate)

    return intersection_coordinates

# Boston example coordinates
# Southwest corner: (42.30, -71.10)
# Northeast corner: (42.40, -71.00)
def get_osm_data(south, west, north, east):
    url = f"https://overpass-api.de/api/interpreter?data=[out:xml];(node({south},{west},{north},{east});way({south},{west},{north},{east});rel({south},{west},{north},{east}););out body;"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None

# Example with Boston
osm_data = get_osm_data(42.30, -71.10, 42.40, -71.00)
