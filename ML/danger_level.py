from intersections import * 

testData = [
    {
      "latitude": 42.3592434,
      "longitude": -71.0936689
    },
    {
      "latitude": 42.3697903,
      "longitude": -71.1125979
    },
    {
      "latitude": 42.37282769999999,
      "longitude": -71.12068649999999
    }
  ]

def getCrashIndex(listCoords: list[dict[int, int]]) -> int:
    for i in range(len(listCoords) - 1):
        lat1, long1 = listCoords[i]["latitude"], listCoords[i]["longitude"]
        lat2, long2 = listCoords[i + 1]["latitude"], listCoords[i + 1]["longitude"]

        south, west, north, east = min(lat1, lat2), min(long1, long2), max(lat1, lat2), max(long1, long2)
        osmData = get_osm_data(south, west, north, east)
        intersectionList = extract_intersections(osmData)
        print(intersectionList)

getCrashIndex(testData)
        
        