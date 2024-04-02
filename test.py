import requests

url = "http://127.0.0.1:5000"

datos = {
    "email": "example2@you",
    "passenger_name" : "PRUEBA FINAL",
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


factory = url + "/factory/create-ticket"

factory_get = url + "/factory/get1"

response = requests.post(url = factory, data = datos)
#response = requests.get(url = factory_get)
print(response.text)
#numero = "hola"

#print(f"{{\"id\": {54}, \"trip\": {26}, \"passenger_name\": \"{"JUAN"}\", \"category\": \"{"ADULTO"}\"}}")