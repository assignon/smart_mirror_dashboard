from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma
from marshmallow import ValidationError
from .authentication_api import login_required

class AppointmentCollection(Resource):
    pass

class AppointmentApi(Resource):
    pass