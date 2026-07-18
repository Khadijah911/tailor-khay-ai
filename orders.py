orders ={
    "ORD001": {
        "customer_name": "Halimah",
        "phone_number": "08031234567",
        "style_description": "Long fitted gown",
        "customer_provided_fabric": False,
        "fabric_details": "Royal blue mesh",
        "price": 55000,
        "amount_paid": 30000,
        "balance": 25000,
        "status": "Pending",
        "delivery_date": "2026-08-10",
        "notes": "Add lycra lining."
    }
}
import json
with open ('orders.json','w') as file:
    json.dump(orders,file,indent=4)