from flask import Blueprint, request, render_template, request, flash, url_for, jsonify
from .models import Ticket, Trip, WebSubscription
from pywebpush import webpush, WebPushException
from datetime import datetime, date, time
from . import db
import json

viewer = Blueprint('viewer', __name__, static_folder= "static/viewer")

@viewer.route("/<int::ticket_id>", methods = ['GET', 'POST'])
def view_ticket(ticket_id):

    ticket = Ticket.query.filter_by(id = ticket_id).first() #Look for the ticket in the database

    if ticket:
        if request.method == 'GET': #View the ticket
                        
                        #https://localhost:5000 + /view/<ticket.id>
            ticket_url = request.host_url[:-1] + url_for("viewer.view_ticket", ticket_id = ticket.id)

            trip = ticket.trip
            print(ticket_url)
            
            #Creates a dictionary for both objects
            ticket_data = ticket.__dict__        
            trip_data = trip.__dict__

            trip_data["date"] = trip.date.strftime("%d-%m-%Y")  #Converts from the date object to a valid string
            trip_data["hour"] = trip.hour.strftime("%H:%M") ##Converts from the hour object to a valid string

            del ticket_data['_sa_instance_state']   #Deletes the sqlalchemy key:value we don't need
            del trip_data['_sa_instance_state']

            ticket_data["trip"] = trip_data
            
            print(ticket_data)
            
            return render_template("viewer/ticket.html", ticket = ticket_data, url = ticket_url)

        elif request.method == 'POST':  #Notifications allowed
            print()
            

        

    # If the ticket exists, view the ticket with a GET method

    # Else if the user's method is POST, enable notifications

    # Else, return message "not found"

    pass


@viewer.route('/service_worker.js', methods=['GET'])
def get_service_worker():
    return viewer.send_static_file('service_worker.js')