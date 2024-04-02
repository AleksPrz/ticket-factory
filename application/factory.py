from flask import Blueprint, request, jsonify
import requests, qrcode
from .models import Ticket, Trip
from . import db
from datetime import datetime

factory = Blueprint('factory', __name__)

@factory.route("/create-ticket", methods = ['POST'])
def create_ticket():

    data = request.form

    #Create trip

    #Create ticket

    #Create qr

    #update the database
    pass


def get_trip(data: dict) -> Trip:
    """Checks if exists a trip with the given atributes
    If exists, returns it
    otherwise, creates a new trip object"""
    
    try: #Formats the datetime data from string to a valid format
        date = datetime.strptime(data.get("date"), "%d-%m-%Y").date() # "01-04-2024" -> date format
        hour = datetime.strptime(data.get("hour"), "%H:%M").time() #"12:00" -> hour format
    except ValueError:
        raise ValueError("Invalid date or hour format")


    trip = Trip.query.filter_by(origin = data.get("origin"),
                                destination = data.get("destination"),
                                date = date,
                                hour = hour,
                                boarding_gate = data.get("boarding_gate")
                                ).first()

    if not trip:
        trip = Trip(origin = data.get("origin"),
                    destination = data.get("destination"),
                    date = date,
                    day = data.get("day"),
                    hour = hour,
                    time = data.get("time"),
                    boarding_gate = data.get("boarding_gate")
                    )
        db.session.add(trip)
        
    return trip


def create_qr(ticket: Ticket) -> str:
    """
    Creates the qr image and saves it locally
    The qr contains plain text that can be converted into a JSON object that contains the following attributes:
    ticket id, trip, passenger name and category
    """

    data = f"{{\"id\": {ticket.id}, \"trip\": {ticket.trip_id}, \"passenger_name\": \"{ticket.passenger_name}\", \"category\": \"{ticket.category}\"}}"

    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)
    qr.add_data(data)
    qr.make(fit = True)

    img = qr.make_image(fill = 'black', back_color = 'white')
    
    url_image = f'application/static/viewer/qr/{ticket.id}.png'
    img.save(url_image)

    return f"../../static/viewer/qr/{ticket.id}.png"


