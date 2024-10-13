from intersections import *
import json

testData2 = [
    {
      "latitude": 42.28608897461656,
      "longitude": -71.09164191096448
    },
    {
      "latitude": 42.31287346648963,
      "longitude": -71.05243806098352
    },
    {
      "latitude": 42.37070952784675,
      "longitude": -71.11276140389808
    }
  ]

testData = [[42.2782195, -71.1599579], [42.2806449, -71.15801549999999], [42.2804387, -71.1575053], 
            [42.28287599999999, -71.1555606], [42.28295809999999, -71.1556179], [42.284184, -71.154533], 
            [42.284093, -71.1543338], [42.2849532, -71.1492689], [42.2855803, -71.14853219999999], 
            [42.2859344, -71.14885869999999], [42.2867813, -71.1310721], [42.2872433, -71.1295566], 
            [42.2871424, -71.127555], [42.2982719, -71.1158051], [42.2979542, -71.1150834], 
            [42.2999512, -71.11359790000002], [42.3284867, -71.0862111], [42.3296042, -71.0861338], 
            [42.3485676, -71.0654176], [42.3588916, -71.0598146], [42.3592295, -71.05951139999999], 
            [42.3596904, -71.0587764], [42.3614983, -71.0575155], [42.36161449999999, -71.0575255], 
            [42.3621363, -71.0566001], [42.3621985, -71.056697], [42.36293510000001, -71.05615879999999], 
            [42.3629781, -71.0562307]] 

sample_crash_data = [
        5,
        [
            2576250,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Cloudy/Cloudy"
        ],
        [
            2637363,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            2618951,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear"
        ],
        [
            3251865,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            3973651,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            3,
            0,
            "Clear"
        ]
    ]

sample_data_2 = [
        10,
        [
            2577005,
            "Unknown",
            "Not Applicable",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            3179577,
            "Not Reported",
            "Not reported",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            3322001,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            1,
            1,
            0,
            "Clear"
        ],
        [
            3432921,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear"
        ],
        [
            3640531,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            2,
            0,
            "Cloudy"
        ],
        [
            4036756,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Not Reported"
        ],
        [
            4363739,
            "Not Reported",
            "Not Applicable",
            2,
            0,
            0,
            "Clear"
        ],
        [
            4376978,
            "Non-fatal injury",
            "Non-fatal injury - Non-incapacitating",
            2,
            1,
            0,
            "Clear/Clear"
        ],
        [
            4433027,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear/Clear"
        ],
        [
            4724993,
            "Property damage only (none injured)",
            "No injury",
            2,
            0,
            0,
            "Clear"
        ]
    ]

def safetyIndex(listCoords: list[str]) ->int:
    crashesInProximity = getCrashIndex(listCoords)

    return statistics.mean(crashesInProximity)

print(safetyIndex(testData))
