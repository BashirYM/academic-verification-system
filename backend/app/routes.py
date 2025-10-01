# backend/app/routes.py
from flask import Blueprint, request
from .controller import waec_request_handler, neco_request_handler, nysc_request_handler

verification_routes = Blueprint('verification_routes', __name__, url_prefix='/api')

@verification_routes.route('/waec', methods=['POST'])
def verify_waec():
    return waec_request_handler(request)

@verification_routes.route('/neco', methods=['POST'])
def verify_neco():
    return neco_request_handler(request)

@verification_routes.route('/nysc', methods=['POST'])
def verify_nysc_route():
    return nysc_request_handler(request)
