from . import db
from flask import Blueprint

viewer = Blueprint('viewer', __name__, static_folder= "static/viewer")

# This decorator specifies the route needed and the HTTP methods available
@viewer.route("/<int::ticket_id>", methods = ['GET', 'POST'])
def view_ticket(ticket_id):

    # Create variable 'ticket' to look for a ticket in the database

    # If the ticket exists, view the ticket with a GET method

    # Else if the user's method is POST, enable notifications

    # Else, return message "not found"

    pass

@viewer.route('/service_worker.js', methods=['GET'])
def sw():

    # Returns a .js file, which is a service worker

    pass