from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
import os
import sys

# models imports

from models.user_model import User
from models.appointment_model import Appointment
from models.guest_model import Guest
from models.image_model import Image

class CreateUser(Resource):
    def post(self):
        User.create()

class GetUser(Resource):
    # @jwt_required
    def get(self):
       return jsonify(User.get_user())