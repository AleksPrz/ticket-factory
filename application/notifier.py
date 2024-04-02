from . import db
from flask import Blueprint, request, jsonify
from .models import Ticket, WebSubscription, Trip