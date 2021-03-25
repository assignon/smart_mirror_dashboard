from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from settings import ma
from marshmallow import ValidationError

# models imports

from models.guest_model import Guest

# schema imports
from schemas.guest_schema import GuestSchema, EditGuestSchema

class GuestCollection(Resource):
    def get(self):
        """
        get all guests
        """
        pass

    def post(self):
        """
        add a new guest
        """
        pass


class Guest(Resource):
    def get(self, guest_id):
        """
        get specific guest
        """
        pass
    

    def put(self, guest_id):
        """
        edit guest
        """
        pass


def remove_whitespace(json_data):
    for key, value in json_data.items():
        if type(value) == str:
            json_data[key] = value.strip()