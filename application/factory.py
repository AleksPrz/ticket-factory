from flask import Blueprint, request, jsonify
import requests, qrcode
from .models import Ticket, Trip
from . import db
from datetime import datetime
from .emailing import send_email

factory = Blueprint('factory', __name__)

@factory.route("/create-ticket", methods = ['POST'])
def create_ticket():
	data = request.form
	trip = get_trip(data)

	new_ticket = Ticket(
		passenger_name = data.get("passenger_name"),
		email = data.get("email"),
		seat_number = data.get("seat_number"),
		category = data.get("category"),
		status = "VIGENTE",     #A new ticket is ACTIVE BY DEFAULT
		service_number = data.get("service_number"),
		operation_number = data.get("operation_number"),
		payment_method = data.get("payment_method"),
		total_payment = data.get("total_payment"),
		billing_token = data.get("billing_token"),
		#wallet_url = "www.com",
		trip = trip
	)

	# We add the new ticket to the database in order to generate its id
	db.session.add(new_ticket) 
	db.session.commit()

	# QR
	new_ticket.qr_url = create_qr(new_ticket)
	db.session.commit()

	# Used to send the data for the email
	user_info = {
		'email_receiver': new_ticket.email,
		'ticket_url': f'http://127.0.0.1:5000/view/{new_ticket.id}',
		'passenger_name': new_ticket.passenger_name
	}

	print(user_info)

	# Send the ticket URL to the user via email
	response = requests.post(url = 'http://127.0.0.1:5000/factory/send-email', data = user_info)
	print(response.text)
	print(new_ticket.id)

	return jsonify({'status': 'sucess', 'message': 'ticket created'})

""" 
This expects this data: email_receiver, ticket_url and passenger_name
"""
@factory.route("/send-email", methods = ['POST'])
def send_ticket_url():
	# Call the function to send the email, passing the data retrieved 
	email_receiver = request.form.get('email_receiver')
	ticket_url = request.form.get('ticket_url')
	passenger_name = request.form.get('passenger_name')

	email_sent_response = send_email(email_receiver, ticket_url, passenger_name)

	if email_sent_response == True:
		return jsonify({'status': 'sucess', 'message': 'email sent succesfully'})
	else:
		return jsonify({'status': 'error', 'message': 'failed to send email'})

def get_trip(data: dict) -> Trip:
	"""Checks if exists a trip with the given atributes
	If exists, returns it,
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