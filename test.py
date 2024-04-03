# Make a POST request to create a ticket using test data

import requests

test_data = {
    "email": "migtorruco@gmail.com",
    "passenger_name" : "Miguel",
    "seat_number" : "12",
    "origin" : "Campeche",
    "destination" : "Guadalajara",
    "date" : "25-03-2024",
    "day" : "LUNES",
    "hour" : "4:40",
    "time" : "TARDE",
    "boarding_gate" : "59",
    "category" : "ADULTO",
    "billing_token" : "123456789",
    "total_payment" : 100.00,
    "payment_method" : "Tarjeta de debito",
    "operation_number" : 56,
    "service_number" : 76
}

factory_url = "http://127.0.0.1:5000/factory/create-ticket"

response = requests.post(url = factory_url, data = test_data)
print(response.text)