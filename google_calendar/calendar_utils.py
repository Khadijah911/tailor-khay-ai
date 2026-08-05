import json

calendar = {
    "2026-07-10":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-12":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-14":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-16":
    {
    "status": "booked",
    "customer_name": 'khadijah',
    "phone_number": '09163456069',
    "time": "10:30 AM",
    "purpose" : 'consultation',
},
    "2026-07-18":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-20":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-22":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-24":
    {
    "status": "booked",
    "customer_name": 'mary',
    "phone_number": '08023882233',
    "time": "11:20 AM",
    "purpose" : 'Measurement',
},
    "2026-07-26":
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
    "2026-07-30": {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
    "purpose" : None,
},
}

with open("calendar.json", "w") as file:
    json.dump(calendar, file, indent=4)