from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from settings import ma
from marshmallow import ValidationError
from .authentication_api import login_required
# models imports

from models.guest_model import Guest

# schema imports
from schemas.guest_schema import GuestSchema, EditGuestSchema

class GuestCollection(Resource):
    @staticmethod
    @login_required
    def get(current_user):
        """
        get all guests
        """
        pass
    
    @staticmethod
    @login_required
    def post(current_user):
        """
        add a new guest
        """
        pass


class Guest(Resource):
    
    @staticmethod
    @login_required
    def get(current_user, guest_id):
        """
        get specific guest
        """
        pass
    
    @staticmethod
    @login_required
    def put(current_user, guest_id):
        """
        edit guest
        """
        pass


def remove_whitespace(json_data):
    for key, value in json_data.items():
        if type(value) == str:
            json_data[key] = value.strip()