measurements = {
    "halimah": {
        "bust": 38,
        "waist": 30,
        "hip": 42,
        "shoulder": 16,
        "sleeve_length": 24,
        "full_length": 58
    },
    "naseemah": {
        "bust": 40,
        "waist": 32,
        "hip": 44,
        "shoulder": 17,
        "sleeve_length": 25,
        "full_length": 60
    },
    "kafco": {
        "bust": 36,
        "waist": 28,
        "hip": 40,
        "shoulder": 15,
        "sleeve_length": 23,
        "full_length": 56
    },
    "zainab": {
        "bust": 42,
        "waist": 34,
        "hip": 46,
        "shoulder": 17,
        "sleeve_length": 26,
        "full_length": 61
    }
}


import json
with open ('measurement.json','w') as file:
   json.dump(measurements,file,indent=4)
