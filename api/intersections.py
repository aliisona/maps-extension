from pyproj import Transformer
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

